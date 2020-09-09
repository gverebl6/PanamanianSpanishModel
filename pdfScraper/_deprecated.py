#System params
URL = sys.argv[1]
ACTAS = sys.argv[2]
ONE_FILE = sys.argv[3]

class deprecated_Scraper():

    def __init__(self, local=False):
        '''
            IMPORTANT: Instalar apt install chromium-chromedriver para VM
        '''
        self._logger = create_logger('pdfScraper-logger')
        self.PARSER = 'lxml'
        self.__tmp_dir = 'pdfScraper/tmp'
        self.storage_manager = StorageManager('pdfs_tesis')
        
        if local:
            self.driver = self.__defineDriver(driver_path='pdfScraper/chromedriver.exe') 
        else: 
            sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
            self.driver = self.__defineDriver() 

        

    def __defineDriver(self, driver_path='chromedriver'):
        """
        This function creates the driver that Selenium uses
        to simulate the browser. 
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
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
            self.storage_manager.upload_object(file_path, f'Acta-{actas}-{year}-{file}')
            self._logger.info(f'File {file_path} extraction completed')
            #timeouut de 10 min entre descargas de archivos.
            time.sleep(600)  

        self.__deletePdfs()  