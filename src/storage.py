from prefect_gcp import GcpCredentials, GcsBucket
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./credentials.json"

from google.cloud import storage

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    try: 
        gcp_credentials = GcpCredentials.load("gcp-stocks-app-credential")

        gcs_bucket = GcsBucket(
            bucket=bucket_name,
            gcp_credentials=gcp_credentials
        )

        gcs_bucket.upload_from_path(source_file_name)

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