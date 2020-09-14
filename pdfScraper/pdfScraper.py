import os
import requests
import time
from bs4 import BeautifulSoup 

import sys
# from selenium import webdriver

# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import TimeoutException

#IMPORT DEL CLOUD MANAGE
from CloudManager.cloudManager import StorageManager
from Logger.logger import create_logger

 
ACTAS = sys.argv[1]

class Scraper():
    def __init__(self):
        
        self._logger = create_logger('pdfScraper_logger')
        self._storage_manager = StorageManager('pdfs_tesis')
        self.__PARSER = 'lxml'
        self.__tmp_dir = 'pdfScraper/tmp'
        self.__base_path = 'https://www.asamblea.gob.pa/'
        
    def __getSoup(self, url):
        """
        Function to get the soup from an url
        """
        r = requests.get(url)
        if r.status_code == 200: 
            return BeautifulSoup(r.text, self.__PARSER)
        else:
            return None
    
    # def __DinamicWait(self, xpath, timeout=10):
    #     """
    #     Creates a Dinamic wait used to wait for a page to load.
    #     """
    #     try:
    #         res = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    #         time.sleep(2)
    #     except:
    #         print('La pagina tardo demasiado....')

    def __deletePdfs(self):
        """
        This method is used to delete all pdfs from the tmp directory
        once all are uploaded to the storage. 
        """
        for file in os.listdir(self.__tmp_dir):
            os.remove(f'{self.__tmp_dir}/{file}')
    
    def _get_actas_path(self, tipo_acta):
        """
            Method that returns the rest of the path based on the type of acta
        """
        url_base = self.__base_path
        #Get path from tipo
        dropdowns = self.__getSoup(url_base)\
            .find('div', attrs={'class': 'region-main-navigation'})\
            .find_all('li')

        for item in dropdowns:
            if item.a.get('href') == '' and item.a.get_text() == 'LABOR LEGISLATIVA':
                menu = item
        
        #print(menu)
        if tipo_acta == 'comision':
            path = menu.find('a', text='Actas de Comisiones').get('href')
        else:
            path = menu.find('a', text='Actas del Pleno').get('href')
        return path

    def extract(self, tipo_acta):
        '''
            Does the extraction of the documents. 
            Recievers tipo_acta with options:
                - comision
                - pleno
        '''
        #Get path depending on type
        path = self._get_actas_path(tipo_acta)
        url_acta = self.__base_path + path
        
        tables = self.__getSoup(url_acta)\
            .find('div', attrs={'class' : 'field--name-field-description'})\
            .find_all('table')
        file_paths = []
        for table in tables:
            for row in table.find_all('tr'):
                try:
                    file_paths.append(row.a.get('href'))   
                except AttributeError:
                    continue


        for path in file_paths:
            file_url = self.__base_path + path[3:]
            file = file_url.split('/')[-1]
            tmp_file = f'{self.__tmp_dir}/{file}'
            try: 
                raw_pdf = requests.get(file_url)
                with open(tmp_file, 'wb') as pdf:
                    pdf.write(raw_pdf.content)
                
                #Codigo para subir en storage
                fecha = file.split('_')[:3]
                storage_object = f'acta_{tipo_acta}_{file.lower()}' 
                self._storage_manager.upload_object(tmp_file, storage_object)
                self._logger.info(f'File {storage_object} extraction completed')
                self.__deletePdfs()  
                # timeouut de 10 min entre descargas de archivos.
            except:
                print('No se pudo descargar el documento...')
            time.sleep(30) 



if __name__ == '__main__':
    
    if ACTAS not in ['comision', 'pleno']:
        print('Tipo de acta invalido....')
        exit()

    scraper = Scraper() #Para correr en Cloud VM
    scraper.extract(tipo_acta=ACTAS)

