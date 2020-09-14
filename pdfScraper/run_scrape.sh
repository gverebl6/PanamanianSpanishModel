#!/bin/bash
echo "Initializing extraction..."
cd ~/PanamanianSpanishModel

#Sujeto a cambio por tarea 8
export GOOGLE_APPLICATION_CREDENTIALS="CloudManager/pr_cred.json"


python -m  pdfScraper.pdfScraper comision
python -m  pdfScraper.pdfScraper pleno
