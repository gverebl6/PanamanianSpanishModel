# PanamanianSpanishModel

Este proyecto se encatga de hacer la extraccion de textos 
para entrenar un modelo de NLP que funciones para 
textos Panameños tomando en cuenta las diferencias que 
existen entre el español general y las perculiaridades 
de como hablamos los panameños.

## Secciones
*   **pdfScraper**: Se encarga de extraer los textos para ser
    almacenados en nuestro storage de Google Cloud Platform.
*   **CloudManager**: En esta parte se encuentran todos los 
    archivos para poder hacer un manejo correcto de nuestro storage en Google Cloud Platform.
*   **textExtractor**: Esta seccion se encarga de extraer los
    pdfs guardados en el storage y extraer los textos 
    necesarios para el entrenamiento del modelo.
*   **ModelTrainer (temporal)**: Parte encargada de la de tomar
    los textos extraidos para hacer el entrenamiento de modelo.

# Execucion
```
Para ejecutar pdfScrapper: 
```
`python -m pdfScraper.pdfScraper comision | pleno`

# Requisitos de instalacion previo al Scrapper: 
Para poder usar Selenium en una maquina virtual sera necesario instalar el chrome driver
en la maquina con el comando: 
`apt install chromium-chromedriver`
Opcional puede ser necesario tener que hacer despues: 
`cp /usr/lib/chromium-browser/chromedriver /usr/bin`


## TODO: 
- [x] Integracion de Cloud con pdfScraper. 
- [ ] Integracion de Cloud con textExtractor. 
- [ ] Definir el nombre final de la seccion de ModelTrainer
- [ ] Llenar el requirements.txt

