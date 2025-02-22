import requests
import pandas as pd
import numpy as np
from src.secret import ALPHA_VANTAGE

def fetch_forex_data(from_symbol: str, to_symbol: str) -> pd.DataFrame:
    """
    Fetch daily Forex data from Alpha Vantage and compute simple and log returns.
    
    Parameters:
    from_symbol (str): The base currency (e.g., 'EUR')
    to_symbol (str): The quote currency (e.g., 'USD')
    
    Returns:
    pd.DataFrame: A DataFrame containing the cleaned Forex data with returns.
    """
    url = (f"https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={from_symbol}"
           f"&to_symbol={to_symbol}&outputsize=full&apikey={ALPHA_VANTAGE}")
    
    r = requests.get(url)
    data = r.json()
    
    # Convert JSON to DataFrame
    df_forex = pd.DataFrame(data['Time Series FX (Daily)']).transpose()
    df_forex = df_forex.reset_index(names="date").rename(
        columns={"1. open": "open", "2. high": "high", "3. low": "low", "4. close": "close"}
    )
    
    # Convert date column to datetime
    df_forex["date"] = pd.to_datetime(df_forex["date"])
    
    # Convert price columns to float
    cols_to_convert = ["open", "high", "low", "close"]
    df_forex[cols_to_convert] = df_forex[cols_to_convert].astype(float)
    
    # Shift data for return calculations
    previous_day = df_forex.iloc[1:].copy()
    last_day = df_forex.iloc[:-1].copy()
    df_forex = df_forex.iloc[:-1]
    
    # Compute simple and log returns
    df_forex.loc[:, "simple_return"] = last_day["close"].to_numpy() / previous_day["close"].to_numpy() - 1
    df_forex.loc[:, "log_return"] = np.log(1 + df_forex["simple_return"])
    
    return df_forex


def fetch_stock_data(symbol: str) -> pd.DataFrame:
    """
    Récupère et nettoie les données journalières d'une action depuis Alpha Vantage.
    
    :param symbol: Le ticker de l'action (ex: "IBM", "AAPL", "TSLA").
    :return: DataFrame avec les prix journaliers et les rendements (simple et log).
    """
    # Construire l'URL pour l'API
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={ALPHA_VANTAGE}"
    
    # Récupération des données
    r = requests.get(url)
    data = r.json()

    # Vérification si l'API a retourné une erreur
    if "Time Series (Daily)" not in data:
        raise ValueError(f"Erreur lors de la récupération des données pour {symbol}: {data}")

    # Conversion en DataFrame
    df = pd.DataFrame(data["Time Series (Daily)"]).transpose()
    
    # Renommage des colonnes
    df = df.reset_index(names="date").rename(columns={
        "1. open": "open",
        "2. high": "high",
        "3. low": "low",
        "4. close": "close",
        "5. volume": "volume"
    })

    # Conversion des types de données
    df["date"] = pd.to_datetime(df["date"])
    cols_to_convert = ["open", "high", "low", "close", "volume"]
    df[cols_to_convert] = df[cols_to_convert].astype(float)

    # Calcul des rendements
    previous_day = df.iloc[1:].copy()
    last_day = df.iloc[:-1].copy()
    
    df = df.iloc[:-1]  # On exclut la première ligne qui n'a pas de précédent

    df.loc[:, "simple_return"] = last_day["close"].to_numpy() / previous_day["close"].to_numpy() - 1
    df.loc[:, "log_return"] = np.log(1 + df["simple_return"])

    return df