import pandas as pd

def carregar_dados(caminho_csv):
    df = pd.read_csv(caminho_csv, sep=";", encoding="utf-8")
    df.columns = [col.strip().replace('\ufeff', '').replace('\r', '').replace('\n', '') for col in df.columns]
    print("COLUNAS ENCONTRADAS:", df.columns.tolist())
    if "Latitude" not in df.columns or "Longitude" not in df.columns:
        raise Exception(f"Colunas Latitude ou Longitude não encontradas! Veja os nomes: {df.columns.tolist()}")
    df["Latitude"] = df["Latitude"].astype(float)
    df["Longitude"] = df["Longitude"].astype(float)
    return df
