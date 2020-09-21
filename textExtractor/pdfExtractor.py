import sys, re, pdfplumber
import os

from CloudManager.cloudManager import StorageManager
from Logger.logger import create_logger

def get_new_docs():
    docs = pdf_storage.get_blobs()
    return [doc for doc in docs if doc.metadata and doc.metadata['extracted'] == 'False']

def change_obj_extention(doc, extention='txt'):
    return f"{doc.split('.')[0]}.{extention}"


def delete_tmp_files(*tmp_directories):
    for directory in tmp_directories:
        for file in os.listdir(directory):
            os.remove(f'{directory}/{file}')

def getPDFNames(path):
    names=[]
    for pdf in os.listdir(tmp_pdfs): #Obteniendo los nombres de los archivos. 
        names.append(pdf)
    return names

def extractingData(pdfsNames,pdfs_path,txts_path):
    files =[]
    for pdf_name in pdfsNames:
        fullText=""
        with pdfplumber.open(pdfs_path+pdf_name) as pdf_reader:
            if len(pdf_reader.pages) > 5:
                
                file_name= txts_path+os.path.splitext(pdf_name)[0]+".txt"
                files.append(file_name)
                
                txt_File = open(file_name,"w+",encoding='utf-8') 
                for page in pdf_reader.pages:
                    if (page.page_number != len(pdf_reader.pages)) and (page.page_number != 1) and (page.page_number != 2):
                        page=page.crop((0,50,0.999*float(page.width),715),relative=True) #Delete the footer and page numbers. 
                        fullText=fullText+page.extract_text()
                final_sentences=re.sub(r'(\–|\-)[A-Z]',"—",fullText)
                final_sentences=re.findall(r'(?:\—|\-)(?:[A-Z\sÑ\.\,ÁÉÍÓÚ]|a\.i\.)*([A-Z\sÑ\.\,ÁÉÍÓÚ][A-Za-z\s\.\…áéíóúüÁÉÍÓÚ\,\¿\?ñÑ0-9\'\"\“\”\:\;\№\(\)\º\°\–\-a-z\‘\¡\!\%\/\&]*)',final_sentences)  
                for sentence in final_sentences:
                    txt_File.write(sentence)
                txt_File.close()
            else:
                print(pdf_name+" no mayor a 3 páginas.")
        
    
    return files



if __name__ == '__main__':

    logger = create_logger('text-extractor')
    #Extraction process
    #Process variables
    tmp_pdfs = sys.argv[1]  #Donde se guardaran los pdfs temporalmente
    tmp_txt = sys.argv[2]   #Donde se guardaran los txt temporalmente
    do_update = int(sys.argv[3]) #Whether or not to extract a file

    #Instanciar los storage managers
    pdf_storage = StorageManager('pdfs_tesis')
    txt_storage = StorageManager('txt_tesis')
    
    #Get all NEW pdf objects
    documents = get_new_docs()
    for doc in documents:

        destination_name = f'{tmp_pdfs}{doc.name}'
        #Download file to temp
        pdf_storage.download_object(
            source_blob_name=doc.name,
            destination_file_path=destination_name
        )

        #Extraction
        try: 
            pdfsNames=getPDFNames(tmp_pdfs)
            files_extracted = extractingData(pdfsNames,tmp_pdfs,tmp_txt)
        except:
            print(f'ERROR: File {pdfsNames[0]} unabled to download...')
            delete_tmp_files(tmp_pdfs, tmp_txt)
            continue
        
        #Upload txt
        if files_extracted:
            new_obj_name = change_obj_extention(doc.name)
            #....Mejorable si se hace por batches....
            txt_storage.upload_object(
                source_file_path=files_extracted[0],
                destination_blob_name=new_obj_name
            )
            logger.info(f'File {files_extracted[0]} extraction completed')
        else: 
            logger.info(f'File {doc.name} not extracted')
            

        #Update pdf
        if do_update:
            pdf_storage.update_blob_extracted(
                blob_name=doc.name,
                file_path=f'{tmp_pdfs}{doc.name}'
            )

        #Eliminar lo de temp

        delete_tmp_files(tmp_pdfs, tmp_txt)


    # # Nueva forma
    # 1. get all blobs(for performance purpouse) \\\\
    # 2. quitar que ya aparecen como extraidos \\\\
    # 3. for blob en blobs \\\
    #     3.1. hacer descarga individual con download blob y guardar en temp \\\
    #     3.2. extraer en temp tambien \\\\
    #     3.3. update_blob \\\
    #     3.4. subir el txt en su bucket \\\ 
    #     3.5. eliminar todo de temp.  \\\
    



