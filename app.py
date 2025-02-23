import json
import numpy as np
import pandas as pd
import yfinance as yf
import streamlit as st
from data.data_loader import tickerf, get_fundamental_info
from utilities.search_bar import get_top10_assets
from sentence_transformers import SentenceTransformer
from widgets.asset_informations import show_stock_informations
from widgets.sidebar import sidebar_widgets



@st.cache_resource
def load_embedder():
    return SentenceTransformer('all-MiniLM-L6-v2')

EMBEDDER = load_embedder()

@st.cache_data
def load_tickers_data():
    tickers_df = pd.read_csv('data/tickers_data.csv')
    tickers_df['embeddings'] = tickers_df['embeddings'].apply(lambda s: np.array(json.loads(s)))
    return tickers_df

TICKERS_DATA = load_tickers_data()


def home_page():
    st.title("Bienvenue sur l'application d'actifs financiers")
    st.write(
        """
        Cette application vous permet de rechercher des données financières sur divers actifs 
        (FOREX, FUTURES, OPTIONS, STOCK, ETF) en utilisant la librairie **yfinance**.
        Sélectionnez une page via les onglets ci-dessus pour accéder aux différentes fonctionnalités.
        """
    )

def asset_selection_page():
    st.title("Recherche d'actif")
    
    # Sélection du type d'actif
    asset_type = st.radio(
        "Sélectionnez le type d'actif :",
        options=["FOREX", "FUTURES", "OPTIONS", "STOCK", "ETF"],
        horizontal=True
    )
    
    # Barre de recherche pour entrer le nom ou le ticker de l'actif
    asset_name = st.text_input("Entrez le nom ou le ticker de l'actif :")
    
    # Bouton de recherche
    if st.button("Rechercher"):
        # Appel à la fonction de recherche et affichage des 10 premiers résultats
        top_assets = get_top10_assets(asset_name, TICKERS_DATA, EMBEDDER)
        # On ne garde que les colonnes Ticker et Name
        resultats = top_assets[['Ticker', 'Name']]
        # Sauvegarde des résultats dans la session pour les conserver entre les réexécutions
        st.session_state['resultats'] = resultats

    # Si des résultats ont été stockés, les afficher
    show_stock_informations()


def main():
    # Ajout de la sidebar avec des widgets
    sidebar_widgets()
    
    # Création des onglets pour la navigation entre les pages
    tabs = st.tabs(["Accueil", "Recherche d'actif"])
    
    with tabs[0]:
        home_page()
    
    with tabs[1]:
        asset_selection_page()

if __name__ == "__main__":
    main()
