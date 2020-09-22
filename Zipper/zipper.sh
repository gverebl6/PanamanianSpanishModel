#!/bin/bash

#This bash file is meant to be run in the gcloudshell

# Params:
NEW_FOLDER=$1 # Folder to download {Like: new_folder}
BUCKET_NAME=$2 # Bucket to download or folder in bucket {gs://bucket}
ZIP_NAME=$3 # Name of the .zip file to create {download.zip}


mkdir $NEW_FOLDER
cd $NEW_FOLDER
gsutil cp -r $BUCKET_NAME .
zip -r $ZIP_NAME .
gsutil cp -r $ZIP_NAME $BUCKET_NAME
gsutil -m acl set -R -a public-read $BUCKET_NAME/$ZIP_NAME
echo "Public URL: "
echo "storage.googleapis.com"/${BUCKET_NAME:5}/$ZIP_NAME