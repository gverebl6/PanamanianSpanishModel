import os, sys
from CloudManager.cloudManager import StorageManager

def get_new_docs():
    docs = pdf_storage.get_blobs()
    return [doc for doc in docs if doc.metadata and doc.metadata['extracted'] == 'False']

def delete_tmp_files(*tmp_directories):
    for directory in tmp_directories:
        for file in os.listdir(directory):
            os.remove(f'{directory}/{file}')

tmp_pdfs = sys.argv[1]  #Donde se guardaran los pdfs temporalmente

pdf_storage = StorageManager('pdfs_tesis')
documents = get_new_docs()
for doc in documents:
    destination_name = f'{tmp_pdfs}{doc.name}'
    #Download documents
    pdf_storage.download_object(
            source_blob_name=doc.name,
            destination_file_path=destination_name
    )

    #Update documents metadata
    pdf_storage.update_blob_extracted(
        blob_name=doc.name,
        file_path=destination_name
    )

delete_tmp_files(tmp_pdfs)