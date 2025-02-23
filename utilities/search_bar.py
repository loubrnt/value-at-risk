import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def get_top10_assets(query_text: str, data, model):
    """
    Retourne les 10 actifs dont le nom est le plus proche du texte de requête.

    Parameters:
        query_text (str): Le texte de la requête.
        data (pd.DataFrame): DataFrame contenant les actifs et leurs embeddings (dans la colonne 'embeddings').
        model (SentenceTransformer): Modèle SentenceTransformer pour encoder la requête.

    Returns:
        pd.DataFrame: Les 10 actifs les plus proches.
    """
    # Calcul de l'embedding pour le texte de la requête
    query_embedding = model.encode(query_text)

    # Calcul de la similarité cosinus entre l'embedding de la requête et chaque embedding de l'actif
    # On transforme la colonne 'embeddings' en tableau numpy pour un calcul vectorisé
    asset_embeddings = np.vstack(data['embeddings'].values)
    similarities = cosine_similarity(asset_embeddings, [query_embedding]).squeeze()

    # Ajout des scores de similarité au DataFrame
    data = data.copy()  # pour ne pas modifier l'original
    data['similarity'] = similarities

    # Tri par similarité décroissante et sélection des 10 meilleurs
    top10 = data.sort_values(by='similarity', ascending=False).head(10)
    return top10