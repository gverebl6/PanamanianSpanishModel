#!/bin/bash

cd PanamanianSpanishModel/pdfScraper/_prev_version/
source venv/bin/activate
export GOOGLE_APPLICATION_CREDENTIALS='/home/gverbel6/PanamanianSpanishModel/CloudManager/cred_google.json'
python pdfscraper.py https://www.asamblea.gob.pa/actas-de-comisiones comision 1 extract