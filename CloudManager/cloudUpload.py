from google.cloud import storage
import requests

'''Para correr el codigo es necesario primero correr el comando: 
    $env:GOOGLE_APPLICATION_CREDENTIALS="[PATH]\[CREDENTIAL_FILE_NAME].json"
''' 

def list_blobs(bucket_name):
    '''
        Lists all the blobs in the bucket.
            bucket_name = "your-bucket-name"
    '''
    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)

    return [blob.name for blob in blobs]

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    ''' Uploads a file to the bucket.
            bucket_name = "your-bucket-name"
            source_file_name = "local/path/to/file"
            destination_blob_name = "storage-object-name"
    '''
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

def download_blob(bucket_name, source_blob_name, destination_file_name):
    ''' Downloads a blob from the bucket.
            bucket_name = "your-bucket-name"
            source_blob_name = "storage-object-name"
            destination_file_name = "local/path/to/file"
    '''
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

if __name__ == '__main__':
    #upload_blob('pdfs_tesis', 'pdfs copy/2020_03_03_V_PLENO.pdf', 'ActaPleno2020_03_03.pdf')
    bucket_name = 'pdfs_tesis'
    current = list_blobs(bucket_name)[0]
    print(current)
    download_blob(bucket_name, current, 'test/retrieved.pdf')
    #download_blob('pdf_tesis', current, 'test/retrieved.pdf')