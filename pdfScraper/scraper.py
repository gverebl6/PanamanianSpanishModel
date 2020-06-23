import requests
import time
from bs4 import BeautifulSoup 
from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from cloudUpload import upload_blob
'''Al usar este file es necesario:
    Para correr el codigo es necesario primero correr el comando: 
        $env:GOOGLE_APPLICATION_CREDENTIALS="[PATH]\[CREDENTIAL_FILE_NAME].json"
''' 

def getSoup(url):
    r = requests.get(url)
    if r.status_code == 200: 
        return BeautifulSoup(r.text, 'lxml')
    else:
        return None

def DinamicWait(driver, xpath, timeout=10):
    try: 
        res = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        time.sleep(2)
    except:
        print('La pagina tardo demasiado....')


def DriverDefinition():
    #Usar Selenium para extraer los nombres de archivos
    driver = webdriver.Chrome(executable_path='chromedriver')
    #Opciones del webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    return driver


def FileNameExtract(driver, url, pages_to_extract=1):
    file_names = []
    #GET a la pagina con la lista
    driver.get(url)

    #Extraer de todas las paginas
    for i in range(pages_to_extract):
        #Espera dinamica a que cargue
        DinamicWait(driver, '//div[@id="titulo"]', timeout=25)
        files = driver.find_elements_by_xpath('//div[@id="titulo"]')
        
        for file in files:
            file_names.append(file.get_attribute('innerHTML'))
        
        next_btn = driver.find_element_by_xpath('//div[@class="next"]')
        next_btn.click()
        
    
    return file_names
        
def pdfDownloader(files):
    for file in files:
    #Obtener url segun el formato de la asamblea. 
        file = file[:-4] + file[-4:].lower()
        year = file[:4]
        decade = int(year)-(int(year) % 10) 
        url_pdf = f'https://www.asamblea.gob.pa/APPS/LEGISPAN/PDF_ACTAS/{decade}_ACTAS/{year}_ACTAS/{year}_ACTAS_PLENO/{file}'

        raw_pdf = requests.get(url_pdf)
        file_path = f'pdfs/{file}'
        with open(file_path, 'wb') as pdf:
            pdf.write(raw_pdf.content)
            
        #Codigo para subir en storage
        upload_blob('pdfs_tesis',file_path,f'Acta_{file[:-12]}.pdf')
        #timeouut de 10 min entre descargas de archivos.
        time.sleep(600)



#-------------------Main------------------------

#La pagina de la asamble tiene un iframe conteniendo el link real de la tabla. 
url_tabla = getSoup('https://www.asamblea.gob.pa/actas-del-pleno').find('iframe').get('src')

#Declarar el driver
driver = DriverDefinition()

file_names = FileNameExtract(driver, url_tabla, pages_to_extract=1)

#print(file_names, len(file_names))

pdfDownloader(file_names)

driver.close()
