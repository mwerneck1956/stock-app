import yfinance as yf
from datetime import datetime, timedelta
from prefect import task, flow
import pandas as pd
import os
from storage import upload_blob
from prefect.artifacts import create_table_artifact
from matplotlib import pyplot as plt
from tenacity import retry, stop_after_attempt, wait_exponential
from prefect.blocks.system import JSON



# Defina o bucket e a lista de tickers
bucket_name = os.getenv("BUCKET_NAME", "stocks-app")
JSON.load("tickers")

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=5))
def fetch_stock_data(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=end_date)
    if df.empty:
        raise ValueError(f"Nenhum dado disponível para {ticker}.")
    return df


@task
def download_stock_data(tickers, start_date, end_date):
    data = {}
    for ticker in tickers:
        try:
            data[ticker] = fetch_stock_data(ticker, start_date, end_date)
            print(f"Dados de {ticker} baixados com sucesso.")
        except Exception as e:
            print(f"Erro ao baixar dados de {ticker} após múltiplas tentativas: {e}")
    return data

@task
def save_partitioned_data(data):
    """
    Salva os dados das ações particionados por dia em arquivos CSV.
    Cada arquivo é enviado para um bucket no Google Cloud.
    """
    base_dir = "data/partitioned"
    os.makedirs(base_dir, exist_ok=True)
    
    for ticker, df in data.items():
        df["Date"] = df.index
        df["Day"] = df["Date"].dt.strftime("%Y-%m-%d")
        
        for day, group in df.groupby("Day"):
            file_path = os.path.join(base_dir, f"{ticker}_{day}.csv")
            print("File path is: ", file_path)
            group.to_csv(file_path, index=False)
            upload_blob(bucket_name,file_path, f"{ticker}/{day}.csv")
            print(f"Dados de {ticker} para {day} salvos em {file_path}.")

@task
def quality_check_and_log(data):
    """
    Realiza uma verificação de qualidade nos dados baixados e registra logs.
    """
    for ticker, df in data.items():
        if df.empty:
            print(f"Nenhum dado para {ticker}. Verifique o ticker ou o intervalo de datas.")
        else:
            print(f"Dados de {ticker} registrados com sucesso. Total de linhas: {len(df)}.")

@task
def calculate_top_movers(data):
    """
    Calcula as 3 ações que mais subiram e as 3 que mais caíram no último dia.
    Cria um artefato com essas informações.
    """
    try:
        last_day_data = {}
        for ticker, df in data.items():
            df["Daily Change"] = df["Close"].pct_change()
            last_day_data[ticker] = df.iloc[-1]["Daily Change"].values[0] if len(df) > 1 else 0

        movers_df = pd.DataFrame.from_dict(last_day_data, orient="index", columns=["Daily Change"])
        movers_df = movers_df.sort_values(by="Daily Change", ascending=False)
        
        top_gainers = movers_df.head(3)
        top_losers = movers_df.tail(3)

        print("Top 3 ações que mais subiram:")
        print(top_gainers)

        print("Top 3 ações que mais caíram:")
        print(top_losers)

        create_table_artifact(
            key="top-movers",
            table=pd.concat([top_gainers, top_losers]).reset_index().to_dict(orient="records"),
            description="Top 3 maiores altas e baixas no último dia.",
        )
    except Exception as e:
        print(f"Erro ao calcular os movimentos do mercado: {e}")


@task
def calculate_moving_average(data, window=3):
    updated_data = {}
    for ticker, df in data.items():
        try:
            df[f"Moving_Avg_{window}"] = df["Close"].rolling(window=window).mean()
            updated_data[ticker] = df
            print(f"Média móvel ({window} dias) calculada para {ticker}.")
        except Exception as e:
            print(f"Erro ao calcular média móvel para {ticker}: {e}")
    return updated_data

@task
def plot_stock_data(data, window=3):
    for ticker, df in data.items():
        try:
            plt.figure(figsize=(10, 6))

            plt.plot(df.index, df["Close"], label="Close", marker="o")
            
            if f"Moving_Avg_{window}" in df.columns:
                plt.plot(df.index, df[f"Moving_Avg_{window}"], label=f"Moving Avg ({window} days)", linestyle="--", color="orange")
        
            plt.title(f"{ticker}: Preços de Fechamento e Média Móvel")
            plt.xlabel("Data")
            plt.ylabel("Preço")
            plt.legend()
            plt.grid()
            plt.tight_layout()
            
            output_dir = "plots"
            os.makedirs(output_dir, exist_ok=True)
            plot_path = os.path.join(output_dir, f"{ticker}_plot.png")
            plt.savefig(plot_path)
            plt.close()
            
            print(f"Gráfico para {ticker} salvo em {plot_path}.")
        except Exception as e:
            print(f"Erro ao plotar gráfico para {ticker}: {e}")
            
@flow(log_prints=True)
def stock_workflow():
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

    data = download_stock_data(tickers, start_date, end_date)
    save_partitioned_data(data)
    quality_check_and_log(data)
    calculate_top_movers(data)

    data_with_moving_avg = calculate_moving_average(data)
    plot_stock_data(data_with_moving_avg)

# Executar o fluxo
if __name__ == "__main__":
    stock_workflow.from_source(
      source="https://github.com/mwerneck1956/stock-app.git",
      entrypoint="src/main.py:stock_workflow"
      ).deploy(
        name ="stock-workflow" , 
        cron = "0 22 * * *", 
        work_pool_name='stock',
        job_variables={"pip_packages": 
            ["yfinance", 
             "prefect", 
             "matplotlib" , 
             "google-api-python-client", 
             "google-cloud",
             "google-cloud-storage",
             "tenacity",
             "prefect-gcp"
             ]}
    )
