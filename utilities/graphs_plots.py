import plotly.graph_objects as go
import numpy as np
from scipy.stats import norm

def plot_return_distribution(df, nbins=300, duration=None, return_type='simple'):
    """
    Affiche la distribution des rendements historiques sous forme d'histogramme 
    avec la courbe gaussienne associée, et ajoute des annotations pour la moyenne et l'écart-type.
    
    Paramètres:
        df (DataFrame): DataFrame contenant les colonnes "simple_return" et "log_return".
        nbins (int): Nombre de bins pour l'histogramme.
        duration (int): Nombre de dernières observations à considérer. Si None, tous les rendements sont pris en compte.
        return_type (str): 'simple' pour utiliser la colonne "simple_return" ou 'log' pour "log_return".
    
    Retour:
        fig (Figure): Objet Figure de Plotly contenant le graphique.
    """
    # Sélection de la série de rendement selon le type choisi
    if return_type == 'simple':
        data = df["simple_return"].dropna()
    elif return_type == 'log':
        data = df["log_return"].dropna()
    else:
        raise ValueError("Le paramètre return_type doit être 'simple' ou 'log'.")

    # Filtrage de la série selon la durée (nombre de dernières observations)
    if duration is not None:
        data = data.tail(duration)
    
    # Calcul de la moyenne (μ) et de l'écart-type (σ)
    mean = data.mean()
    std = data.std()

    # Création de la figure Plotly
    fig = go.Figure()

    # Ajout de l'histogramme
    fig.add_trace(go.Histogram(
        x=data,
        nbinsx=nbins,
        marker=dict(
            color="royalblue",
            line=dict(width=1.2, color="black")
        ),
        opacity=0.75,
        showlegend=False
    ))

    # Calcul et ajout de la courbe gaussienne
    x_values = np.linspace(data.min(), data.max(), 1000)
    pdf = norm.pdf(x_values, loc=mean, scale=std)
    bin_width = (data.max() - data.min()) / nbins
    scaled_pdf = pdf * len(data) * bin_width

    fig.add_trace(go.Scatter(
        x=x_values,
        y=scaled_pdf,
        mode='lines',
        line=dict(color='red', width=2),
        name=f'Gaussienne (μ={mean:.2%}, σ={std:.2%})'
    ))

    # Ligne verticale pour la moyenne (μ)
    fig.add_shape(
        type="line",
        x0=mean, x1=mean,
        y0=0, y1=max(scaled_pdf),
        line=dict(color="lime", dash="dash")
    )
    fig.add_annotation(
        x=mean,
        y=max(scaled_pdf)*0.9,
        text=f"μ: {mean:.2%}",
        showarrow=True,
        arrowhead=2,
        ax=40,
        ay=-40,
        font=dict(color="lime")
    )

    # Lignes verticales pour μ - σ et μ + σ
    fig.add_shape(
        type="line",
        x0=mean - std, x1=mean - std,
        y0=0, y1=max(scaled_pdf),
        line=dict(color="orange", dash="dot")
    )
    fig.add_annotation(
        x=mean - std,
        y=max(scaled_pdf)*0.7,
        text=f"μ - σ: {(mean - std):.2%}",
        showarrow=True,
        arrowhead=2,
        ax=-40,
        ay=-40,
        font=dict(color="orange")
    )

    fig.add_shape(
        type="line",
        x0=mean + std, x1=mean + std,
        y0=0, y1=max(scaled_pdf),
        line=dict(color="orange", dash="dot")
    )
    fig.add_annotation(
        x=mean + std,
        y=max(scaled_pdf)*0.7,
        text=f"μ + σ: {(mean + std):.2%}",
        showarrow=True,
        arrowhead=2,
        ax=40,
        ay=-40,
        font=dict(color="orange")
    )

    # Mise en forme du graphique
    fig.update_layout(
        title="Distribution des Rendements Quotidiens",
        xaxis_title="Rendement Quotidien",
        yaxis_title="Nombre de Jours",
        xaxis=dict(tickformat=".2%"),
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.93,
            xanchor="left",
            x=0.1
        )
    )

    return fig