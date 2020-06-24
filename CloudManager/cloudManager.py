"""
In here we have all the code needed to manage GCP Storage
"""
import os
import platform
from google.cloud import storage

class StorageManager():

    def __init__(self, bucket_name,credential_path='proy_cred.json'):

        warning =   """
                    This class is in charge of managing the GCP storage. 
                        
                    IMPORTANT: In order to be able to authenticate it is required that
                    the user run the {credential_command} on console.
                        (For future an automatic run will be implemented.)
                    
                    """

        credential_path = os.path.abspath(credential_path)

        self.__windows_command = f'$env:GOOGLE_APPLICATION_CREDENTIALS="{credential_path}"'
        self.__linux_command =f'export GOOGLE_APPLICATION_CREDENTIALS="{credential_path}"'
        self.bucket_name = bucket_name

        if platform.system() == 'Windows':
            self.credential_command = self.__windows_command
        else:
            self.credential_command = self.__linux_command

        print(warning)

    def list_storage_objects(self):
        """
        Lists all the blobs (objects) in the bucket.
            bucket_name: Name of the storage bucket. As: pdfs
        """
        storage_client = storage.Client()
        # Note: Client.list_blobs requires at least package version 1.17.0.
        blobs = storage_client.list_blobs(self.bucket_name)

        return [blob.name for blob in blobs]
    
    def upload_object(self, source_file_path, destination_blob_name):
        ''' Uploads a file to the bucket.
                source_file_path = "local/path/to/file"
                destination_blob_name = "storage-object-name"
        '''
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_path)


    def download_object(self, source_blob_name, destination_file_path):
            ''' Downloads a blob from the bucket.
                    source_blob_path = "storage-object-name"
                    destination_file_name = "local/path/to/file"
            '''
            storage_client = storage.Client()

            bucket = storage_client.bucket(self.bucket_name)
            blob = bucket.blob(source_blob_name)

            blob.download_to_filename(destination_file_path)



if __name__ == '__main__':
    storage_manager = StorageManager(bucket_name='pdfs_tesis')
    print(storage_manager.credential_command)
    # objects = storage_manager.list_storage_objects()
    # storage_manager.download_object(source_blob_name=objects[0], destination_file_path='test\\test_sownload.pdf')
    # storage_manager.upload_object(source_file_path='test\\2020_03_10_V_PLENO.pdf', destination_blob_name='ActaPleno2020_03_10_test.pdf')


    

    
