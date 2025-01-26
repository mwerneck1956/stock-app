from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
from google.cloud import storage
from google.oauth2 import service_account
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./credentials.json"

# Escopo para acessar o Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.file']


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
    # Exemplo de uso
    #drive_service = authenticate_google_drive()

    # Substitua pelo caminho do arquivo que deseja enviar (deve estar no mesmo folder de execução do script)
    #file_to_upload = "./src/example-2.txt"

    # Substitua pelo ID da pasta no Google Drive (ou deixe como None para enviar na raiz)
    # O folder_id pode ser encontrado clicando no Drive em Compartilhar Link
    # Ex. do meu: https://drive.google.com/drive/folders/1oDw-8sjy3CnIE4bEKe52lyBpWV8UcXGz?usp=drive_link
    #folder_id = "1Nf4ie8Y3rHNzmlivdszp_cTlSI3uu9Da"

    #uploaded_file = upload_to_drive(drive_service, file_to_upload, folder_id)
    #print(f"Arquivo enviado com sucesso! ID: {uploaded_file['id']}, Nome: {uploaded_file['name']}")
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    bucket_name = "stocks-app"
    # The path to your file to upload
    source_file_name = "./src/example-2.txt"
    # The ID of your GCS object
    destination_blob_name = "storage-object-name"

    upload_blob(bucket_name, source_file_name, destination_blob_name)