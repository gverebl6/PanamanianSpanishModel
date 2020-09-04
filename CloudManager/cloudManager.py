"""
In here we have all the code needed to manage GCP Storage
"""
import os
import platform
from google.cloud import storage

class StorageManager():

    def __init__(self, bucket_name):

        warning =   """
                    This class is in charge of managing the GCP storage. 
                        
                    IMPORTANT: In order to be able to authenticate it is required that
                    the user run the {credential_command} on console.
                        (For future an automatic run will be implemented.)
                    
                    """

        self.bucket_name = bucket_name

        print(warning)

    @staticmethod
    def credential_command(credential_path='proy_cred.json'):
        '''
        Prints the command to execute to validate credential depending on OS.
        '''
        credential_path = os.path.abspath(credential_path)

        if platform.system() == 'Windows':
            return f'Credential command: $env:GOOGLE_APPLICATION_CREDENTIALS="{credential_path}"'
        else:
            return f'Credential command: export GOOGLE_APPLICATION_CREDENTIALS="{credential_path}"'
            
    def get_blobs(self):
        """
        Returns all the blobs with their metadata
        """
        storage_client = storage.Client()
        blobs = storage_client.list_blobs(self.bucket_name)
        return blobs

    def get_blob(self, blob_name):
        """
        Returns a specific blob
        """
        storage_client = storage.Client()
        blobs = storage_client.list_blobs(self.bucket_name)
        blob = [blob for blob in blobs if blob.name == blob_name][0]
        return blob

    def list_storage_objects(self):
        """
        Lists all the blobs (objects) in the bucket.
        """
        storage_client = storage.Client()
        # Note: Client.list_blobs requires at least package version 1.17.0.
        blobs = storage_client.list_blobs(self.bucket_name)

        return [blob.name for blob in blobs]
    
    def upload_object(self, source_file_path, destination_blob_name, extracted=False):
        ''' Uploads a file to the bucket.
                source_file_path = path to the file to be uploaded on the storage bucket
                destination_blob_name = name used to store file in the storage bucket
        '''
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.metadata = {'extracted': extracted}

        blob.upload_from_filename(source_file_path)

        print(f'File: {source_file_path} subido como {destination_blob_name}')

    def update_blob_extracted(self, blob_name, file_path):
        """
        Updates the blobs metadata to indicate it has been extracted already
        params: 
            file_path: Path of the file to be updated
            blob_name: name of the blob on storage to be updated
        """
        self.upload_object(file_path, blob_name, extracted=True )

    def download_object(self, source_blob_name, destination_file_path):
        ''' Downloads a blob from the bucket.
                source_blob_path = name of the stored object 
                destination_file_name = path where file will be downloaded
        '''
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket_name)
        blob = bucket.blob(source_blob_name)

        blob.download_to_filename(destination_file_path)

        print(f'Blob: {source_blob_name} descargado en {destination_file_path}')


    def delete_object(self, source_blob_name):
        ''' Deletes a blob in GCP:
                source_blob_name: file/blob name in storage bucket
        '''
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.delete()

        print(f'Blob: {source_blob_name} eliminado')




        


if __name__ == '__main__':
    storage_manager = StorageManager(bucket_name='pdfs_tesis')
    print(storage_manager.credential_command)
    # objects = storage_manager.list_storage_objects()
    # storage_manager.download_object(source_blob_name=objects[0], destination_file_path='test\\test_sownload.pdf')
    # storage_manager.upload_object(source_file_path='test\\2020_03_10_V_PLENO.pdf', destination_blob_name='ActaPleno2020_03_10_test.pdf')


    

    
