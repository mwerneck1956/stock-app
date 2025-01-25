import yfinance as yf
from datetime import datetime, timedelta
from prefect import task, flow
import pandas as pd
import os
from datetime import datetime, timedelta
from storage import upload_blob

from prefect.artifacts import create_link_artifact


bucket_name = os.getenv("BUCKET_NAME", "stocks-app")

# Defina as variáveis de data e os tickers
start_date = '2024-01-01'
end_date = '2024-12-31'
tickers = ["GOOGL", "AAPL"]



@task
def download_stock_data(tickers, start_date, end_date, log_prints=True):
    data = {}
    for ticker in tickers:
        df = yf.download(ticker, start=start_date, end=end_date)
        data[ticker] = df
        print(f"Dados de {ticker} baixados com sucesso {df['Close']}")
    return data

@task
def upload_to_drive_and_create_link(data):
    links = {}
    for ticker, df in data.items():
        file_path = os.path.join(f"{ticker}_stock_data.csv")
        df['Close'].to_csv(file_path)

        upload_blob(bucket_name=bucket_name, source_file_name=file_path, destination_blob_name=file_path)
        print(f"Dados de {ticker} salvos em {file_path}")

        links[ticker] = file_path
        process_data(df['Close'])

        create_link_artifact(
            key=ticker.lower(),
            link=file_path,
            description=ticker + "stock_data",
        )

    return links

@flow
def process_data(tickers):
    for stockPrice in tickers:
      print(f"hs {stockPrice} ")

@flow
def stock_workflow():
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

    data = download_stock_data(tickers, start_date, end_date)
    artifact_links = upload_to_drive_and_create_link(data)

    for ticker, link in artifact_links.items():
        print(f"Link para os dados de {ticker}: {link}")

# Executar o fluxo
if __name__ == "__main__":
      #stock_workflow()
      stock_workflow.serve(name ="stock-workflow" , cron = "0 19 * * *")
