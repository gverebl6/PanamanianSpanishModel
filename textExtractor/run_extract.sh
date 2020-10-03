#!/bin/bash
echo "Initializing extraction..."
cd ~/PanamanianSpanishModel

#Sujeto a cambio por tarea 8
export GOOGLE_APPLICATION_CREDENTIALS='/home/gverbel/Proyectos/Tesis/PanamanianSpanishModel/CloudManager/cred_google.json'


python -m textExtractor.pdfExtractor\
    ./textExtractor/tmp/pdf/\
    ./textExtractor/tmp/txt/\ 
    1 # dor true