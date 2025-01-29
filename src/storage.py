from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
from google.cloud import storage
from google.oauth2 import service_account
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./credentials.json"

from google.cloud import storage

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    try: 
        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        # Faz o upload do arquivo
        blob.upload_from_filename(source_file_name)

        print(f"Arquivo {source_file_name} foi enviado para {destination_blob_name} no bucket {bucket_name}.")
    except Exception as e:
        print(f"Erro ao fazer upload: {e}")



if __name__ == "__main__":
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    bucket_name = "stocks-app"
    # The path to your file to upload
    source_file_name = "./src/example-2.txt"
    # The ID of your GCS object
    destination_blob_name = "storage-object-name"

    upload_blob(bucket_name, source_file_name, destination_blob_name)