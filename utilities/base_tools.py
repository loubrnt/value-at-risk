import pandas as pd
import numpy as np

def compute_returns(df):
    """
    Calcule les retours quotidiens simples et logarithmiques à partir de la colonne 'Close'
    du DataFrame. Le DataFrame est supposé contenir une colonne 'Date' (de type datetime ou string)
    et une colonne 'Close'.
    
    Paramètres:
        df (pd.DataFrame): DataFrame contenant au minimum les colonnes 'Date' et 'Close'.
        
    Retour:
        pd.DataFrame: DataFrame d'origine avec deux nouvelles colonnes:
                      - 'Simple Return' : Retour simple calculé comme (Close_i / Close_{i-1}) - 1
                      - 'Log Return'    : Retour logarithmique calculé comme ln(Close_i / Close_{i-1})
    """
    # On s'assure que le DataFrame est trié par date
    df = df.sort_values('Date').reset_index(drop=True)
    
    # Calcul du retour simple
    df['simple_return'] = df['Close'].pct_change()
    
    # Calcul du retour logarithmique
    df['log_return'] = np.log(df['Close'] / df['Close'].shift(1))
    
    return df.iloc[1:]
