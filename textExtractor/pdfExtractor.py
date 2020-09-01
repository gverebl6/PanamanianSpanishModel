import sys, re, pdfplumber
import os

def getPDFNames(path):
    Names=[]
    for pdf in os.listdir(pdfs_path): #Obteniendo los nombres de los archivos. 
        Names.append(pdf)
    return Names

def extractingData(pdfsNames,pdfs_path,txts_path):
    for pdf_name in pdfsNames:
        fullText=""
        pdf_reader=pdfplumber.open(pdfs_path+pdf_name)

        if len(pdf_reader.pages) > 5:
            txt_File = open(txts_path+os.path.splitext(pdf_name)[0]+".txt","w+",encoding='utf-8') 
            for page in pdf_reader.pages:
                if (page.page_number != len(pdf_reader.pages)) and (page.page_number != 1) and (page.page_number != 2): 
                    print("Page Number: "+str(page.page_number))
                    print("Page Width "+str(page.width))
                    print("Page Height "+str(page.height))
                    page=page.crop((0,50,0.999*float(page.width),715),relative=True) #Delete the footer and page numbers. 
                    #page=page.within_bbox((1,50,612,715),relative=True)
                    fullText=fullText+page.extract_text()
            final_sentences=re.sub(r'(\–|\-)[A-Z]',"—",fullText)
            final_sentences=re.findall(r'(?:\—|\-)(?:[A-Z\sÑ\.\,ÁÉÍÓÚ]|a\.i\.)*([A-Z\sÑ\.\,ÁÉÍÓÚ][A-Za-z\s\.\…áéíóúüÁÉÍÓÚ\,\¿\?ñÑ0-9\'\"\“\”\:\;\№\(\)\º\°\–\-a-z\‘\¡\!\%\/\&]*)',final_sentences)  
            for sentence in final_sentences:
                txt_File.write(sentence)
            txt_File.close()
        else:
            print(pdf_name+" no mayor a 3 páginas.")



if __name__ == '__main__':
    pdfs_path=sys.argv[1] #De donde se sacaran los PDF.
    txts_path=sys.argv[2] #Donde se guardará la DATA cleaned. 
    pdfsNames=getPDFNames(pdfs_path)
    extractingData(pdfsNames,pdfs_path,txts_path)



    



