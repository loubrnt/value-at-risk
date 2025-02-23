import yfinance as yf

def get_long_business_summary(ticker: str):
    """
    Retrieve the long business summary for a given ticker.

    Args:
        ticker (str): The ticker symbol (e.g., 'ABEQ').

    Returns:
        str: The long business summary if available, or None otherwise.
    """
    try:
        tkr = yf.Ticker(ticker)
        info = tkr.info
        summary = info.get('longBusinessSummary')
        if summary:
            return summary
        else:
            print(f"No long business summary found for ticker: {ticker}")
            return None
    except Exception as e:
        print(f"Error retrieving long business summary for ticker {ticker}: {e}")
        return None
    
def tickerf(ticker: str):
    """
    Retrieve historical data for a given ticker over the last 5 years.

    Args:
        ticker (str): The ticker symbol (e.g., 'ABEQ').

    Returns:
        DataFrame: A DataFrame containing historical data (Open, High, Low, Close, Volume, etc.),
                   or None if no data is found.
    """
    try:
        # Create a Ticker object
        tkr = yf.Ticker(ticker)
        # Retrieve historical data over the past 5 years
        hist = tkr.history(period="5y")
        if hist.empty:
            print(f"No data found for ticker: {ticker}")
            return None
        return hist.reset_index()
    except Exception as e:
        print(f"Error retrieving data for ticker {ticker}: {e}")
        return None
    

def get_fundamental_info(ticker_symbol):
    """
    Récupère les informations fondamentales d'une entreprise à partir de son ticker.

    Args:
        ticker_symbol (str): Le symbole boursier de l'entreprise (ex: "AAPL" pour Apple).

    Returns:
        dict: Un dictionnaire contenant le nom de l'entreprise, le secteur, l'industrie,
              la capitalisation boursière et un résumé de l'activité.
    """
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    
    return {
        "Nom de l'entreprise": info.get("longName"),
        "Secteur": info.get("sector"),
        "Industrie": info.get("industry"),
        "Capitalisation boursière": info.get("marketCap"),
        "Résumé de l'activité": info.get("longBusinessSummary")
    }