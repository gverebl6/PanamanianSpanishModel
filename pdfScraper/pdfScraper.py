import os
import requests
import time
from bs4 import BeautifulSoup 
from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

#IMPORT DEL CLOUD MANAGE
from CloudManager.cloudManager import StorageManager

 
    #Usamos esta constante porque en Linux puede que sea necesario hacer el cambio

class Scraper():

    def __init__(self, driver_exe_path):
        '''
            driver_exe_path: Path to the webdriver.exe
        '''
        self.driver = self.__defineDriver(driver_exe_path) 
        self.PARSER = 'lxml'
        self.__tmp_dir = 'pdfScraper/tmp'
        self.storage_manager = StorageManager('pdfs_tesis')

    def __defineDriver(self, driver_path):
        """
        This function creates the driver that Selenium uses
        to simulate the browser. 
        """
        driver = webdriver.Chrome(executable_path=driver_path)
        options = webdriver.ChromeOptions()
        options.add_argument('--incognito')
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
            os.remove(f'{self.__tmp_dir}\\{file}')
        


    def extract(self, url, actas='pleno', pages=1, one_file=False):
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


        for file in file_names[:last]:
            #Uttilizamos el nombre del archivo para generar el url
            file = file[:-4] + file[-4:].lower()
            year = file[:4]
            decade = int(year)-(int(year) % 10) 
            if actas=='pleno':
                url_pdf = f'https://www.asamblea.gob.pa/APPS/LEGISPAN/PDF_ACTAS/{decade}_ACTAS/{year}_ACTAS/{year}_ACTAS_PLENO/{file}'
            else:
                url_pdf = f'https://www.asamblea.gob.pa/APPS/LEGISPAN/PDF_ACTAS/{decade}_ACTAS/{year}_ACTAS/{year}_ACTAS_COMISION/{year}_COMISION/{file}'

            raw_pdf = requests.get(url_pdf)
            file_path = f'{self.__tmp_dir}\\{file}'
            with open(file_path, 'wb') as pdf:
                pdf.write(raw_pdf.content)
                
            #Codigo para subir en storage
            self.storage_manager.upload_object(file_path, f'Acta{file}')

            #timeouut de 10 min entre descargas de archivos.
            time.sleep(600)  

        self.__deletePdfs()  

                   


if __name__ == '__main__':
    scraper = Scraper('pdfScraper/chromedriver.exe')
    scraper.extract(url= 'https://www.asamblea.gob.pa/actas-de-comisiones', actas='comision', one_file=True)
    scraper.driver.close()