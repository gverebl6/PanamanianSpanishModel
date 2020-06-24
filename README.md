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

#Execucion
> Para ejecutar pdfScrapper: `python -m pdfScraper.pdfScraper`

## TODO: 
- [ ] Integracion de Cloud con las demas secciones. 
- [ ] Definir el nombre final de la seccion de ModelTrainer
- [ ] Llenar el requirements.txt