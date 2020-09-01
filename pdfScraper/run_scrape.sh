#!/bin/bash
echo "Initializing extraction..."
cd ~/PanamanianSpanishModel

#Sujeto a cambio por tarea 8
export GOOGLE_APPLICATION_CREDENTIALS="{credential_path}" 

echo "Downloading Driver..."
apt install chromium-chromedriver

python -m  pdfScraper.pdfScraper\
    https://www.asamblea.gob.pa/actas-de-comisiones\
    comisiones\
    False

