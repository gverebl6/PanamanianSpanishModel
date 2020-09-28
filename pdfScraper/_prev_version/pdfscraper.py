import os
import requests
import time
from bs4 import BeautifulSoup 

import sys
from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

#IMPORT DEL CLOUD MANAGE

from cloudManager import StorageManager
#from Logger.logger import create_logger


#System params
URL = sys.argv[1]
ACTAS = sys.argv[2]
PAGES = sys.argv[3]
ACTION = sys.argv[4]

class deprecated_Scraper():

    def __init__(self, local=False):
        '''
            IMPORTANT: Instalar apt install chromium-chromedriver para VM
        '''
        #self._logger = create_logger('pdfScraper-logger')
        self.PARSER = 'lxml'
        self.__tmp_dir = './tmp'
        self._storage_manager = StorageManager('pdfs_tesis')
        
        if local:
            self.driver = self.__defineDriver(driver_path='./chromedriver.exe') 
        

        

    def __defineDriver(self, driver_path='chromedriver'):
        """
        This function creates the driver that Selenium uses
        to simulate the browser. 
        """
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--incognito')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(driver_path,chrome_options=chrome_options)
        return driver

    def __getSoup(self, url):
        """
        Function to get the soup from an url
        """
        r = requests.get(url)
        if r.status_code == 200: 
            return BeautifulSoup(r.text, self.PARSER)
        else:
            return None

    def __DinamicWait(self, xpath, timeout=10):
        """
        Creates a Dinamic wait used to wait for a page to load.
        """
        try:
            res = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            time.sleep(2)
        except:
            print('La pagina tardo demasiado....')
    
    def __extractActasPleno(self, url, pages):
        """
        Extracts files from 'Actas del Pleno'
        """
        file_names = []
        self.driver.get(url) #Le hacemos GET a la pagina con la lista
        
        for i in range(pages):
            self.__DinamicWait('//div[@id="titulo"]', timeout=25)
            files = self.driver.find_elements_by_xpath('//div[@id="titulo"]')
            for file in files:
                file_names.append(file.get_attribute('innerHTML'))
            
            next_btn = self.driver.find_element_by_xpath('//div[@class="next"]')
            next_btn.click()
        
        return file_names

    def __extractActasComisiones(self, url, pages):
        """
        Extracts files from 'Actas de Comisiones'
        """
        file_names = []
        self.driver.get(url) #Le hacemos GET a la pagina con la lista
        
        #El orden en comisiones es diferente por lo que necesitamos
        #irnos al ultimo y echar para atras para ir de los mas recientes 
        #a los mas viejos.
        self.__DinamicWait('//div[@id="titulo"]', timeout=25)
        last_btn = self.driver.find_element_by_xpath('//div[@class="last"]')
        last_btn.click()

        for i in range(pages+1):
            self.__DinamicWait('//div[@id="titulo"]', timeout=25)

            files = self.driver.find_elements_by_xpath('//div[@id="titulo"]')
            for file in files:
                file_names.append(file.get_attribute('innerHTML'))
            
            next_btn = self.driver.find_element_by_xpath('//div[@class="prev"]')
            next_btn.click()
        
        return file_names

    def __deletePdfs(self):
        """
        This method is used to delete all pdfs from the tmp directory
        once all are uploaded to the storage. 
        """
        for file in os.listdir(self.__tmp_dir):
            os.remove(f'{self.__tmp_dir}/{file}')
        


    def get_links(self, url, actas='pleno', pages=1, one_file=False, link_file=None):
        table_url = self.__getSoup(url).find('iframe').get('src')
        if actas=='pleno': 
            file_names = self.__extractActasPleno(table_url, pages)
        else:
            file_names = self.__extractActasComisiones(table_url, pages)

        #This is used for the option to only download one
        if one_file:
            last = 1
        else:
            last = len(file_names)

        links = []

        for file in file_names[:last]:
            #Uttilizamos el nombre del archivo para generar el url
            file = file[:-4] + file[-4:].lower()
            year = file[:4]
            decade = int(year)-(int(year) % 10) 
            if actas=='pleno':
                url_pdf = f'https://www.asamblea.gob.pa/APPS/LEGISPAN/PDF_ACTAS/{decade}_ACTAS/{year}_ACTAS/{year}_ACTAS_PLENO/{file}'
            else:
                url_pdf = f'https://www.asamblea.gob.pa/APPS/LEGISPAN/PDF_ACTAS/{decade}_ACTAS/{year}_ACTAS/{year}_ACTAS_COMISION/{year}_COMISION/{file}'

            links.append(url_pdf)

            
        with open(link_file, 'w') as f:
            for link in links:
                f.write(f'{link}\n')



    
    def extract(self, link_file, tipo_acta):
        with open(link_file, 'r') as file:
            links = file.readlines()
            links = [link.strip() for link in links]
        
        for link in links:
            file = link.split('/')[-1] #File url
            tmp_file = f'{self.__tmp_dir}/{file}' #tmp_file_path
            storage_object = f'acta_{tipo_acta}_{file}' #File name in Storage
            
            print(f'Extracting {file} from {link}')
            print(tmp_file)
            try:
                raw_pdf = requests.get(link)
                with open(tmp_file, 'wb') as pdf:
                    pdf.write(raw_pdf.content)
            except:
                print('No se pudo descargar el documento...')

            self._storage_manager.upload_object(tmp_file, storage_object)
            #self._logger.info(f'File {storage_object} extraction completed')
            self.__deletePdfs()  
            
            
                





if __name__ == '__main__':

    if ACTION == 'get_files':
        scraper = deprecated_Scraper(local=True)
        scraper.get_links(url=URL, actas=ACTAS, pages=int(PAGES), link_file='./links.txt')
        scraper.driver.close()
    else:
        scraper = deprecated_Scraper(local=False)
        scraper.extract(link_file='./links.txt', tipo_acta=ACTAS)

    