from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
from google.cloud import storage
from google.oauth2 import service_account
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./credentials.json"

# Escopo para acessar o Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.file']


def authenticate_google_drive():
    """
    Autentica o usuário com o Google Drive usando uma conta de serviço.
    Retorna o serviço do Google Drive para operações de API.

    O credentials file pode ser obtido criando uma Service Account em IAM & Admin, no Google Console.
    """
    credentials = Credentials.from_service_account_file(
        './src/credentials.json', scopes=SCOPES
    )
    return build('drive', 'v3', credentials=credentials)


def upload_to_drive(service, file_path, folder_id=None):
    """
    Faz upload de um arquivo genérico para o Google Drive.

    Args:
        service: Serviço autenticado do Google Drive.
        file_path (str): Caminho do arquivo a ser enviado.
        folder_id (str, opcional): ID da pasta onde o arquivo será enviado. Default é None.

    Returns:
        dict: Informações do arquivo enviado, incluindo ID e nome.
    """
    file_name = os.path.basename(file_path)

    # Configura os metadados do arquivo
    file_metadata = {'name': file_name}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    # Prepara o arquivo para upload
    media = MediaFileUpload(file_path, resumable=True)

    # Faz o upload
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name'
    ).execute()

    return file


from google.cloud import storage



def upload_blob(bucket_name, source_file_name, destination_blob_name):
    try: 
        storage_client = storage.Client()
    

        bucket = storage_client.bucket(bucket_name)

        # Cria o objeto blob (arquivo no bucket)
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