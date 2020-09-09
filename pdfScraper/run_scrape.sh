#!/bin/bash
echo "Initializing extraction..."
cd ~/PanamanianSpanishModel

#Sujeto a cambio por tarea 8
export GOOGLE_APPLICATION_CREDENTIALS="{credential_path}" 


python -m  pdfScraper.pdfScraper comision
python -m  pdfScraper.pdfScraper pleno
