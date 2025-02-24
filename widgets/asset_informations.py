import streamlit as st
import plotly.express as px
from data.data_loader import tickerf, get_fundamental_info
from utilities.graphs_plots import plot_return_distribution
from utilities.base_tools import compute_returns

def show_stock_informations():
    if 'resultats' in st.session_state:
        st.divider()
        st.write("### Liste des resultats les plus pertinents:")
        st.dataframe(st.session_state['resultats'], width=1000)
        
        # Création d'une liste d'options pour le sélecteur
        options = st.session_state['resultats'].apply(lambda row: f"{row['Ticker']} - {row['Name']}", axis=1).tolist()
        st.selectbox("Sélectionnez l'actif qui vous intéresse :", options, key="selected_asset")
        
        # Affichage des informations historiques si le bouton est cliqué ou si déjà affiché
        if st.button("Afficher les informations historiques") or st.session_state.get("display_history", False):
            st.session_state.display_history = True
            
            # Extraction du ticker et du nom depuis la sélection (format "TICKER - Name")
            ticker_selected = st.session_state.selected_asset.split(" - ")[0]
            asset_name = st.session_state.selected_asset.split(" - ")[1] if " - " in st.session_state.selected_asset else ticker_selected
            
            st.markdown(f"## Informations fondamentales pour **{ticker_selected}**")
            fundamental_info = get_fundamental_info(ticker_selected)
            
            # Affichage des informations fondamentales dans des expandeurs
            for key, value in fundamental_info.items():
                with st.expander(f"{key}", expanded=True):
                    if key == "Capitalisation boursière":
                        formatted_value = f"<span style='color:green'>{format(int(value), ',')} $</span>"
                        st.markdown(formatted_value, unsafe_allow_html=True)
                    else:
                        st.write(value)
            
            st.divider()
            hist_data = tickerf(ticker_selected)
            if hist_data is not None:
                st.markdown(f"## Historique du cours pour **{ticker_selected}**")
                st.dataframe(hist_data)
                
                st.markdown("## Paramètres des graphiques")
                # Formulaire global pour les deux graphiques
                with st.form(key="all_graphs"):
                    st.markdown("### Distribution des returns")
                    days_dist = st.slider("Nombre de jours à prendre en compte (distribution)",
                                          min_value=1, 
                                          max_value=len(hist_data), 
                                          value=min(252, len(hist_data)))
                    return_type = st.radio("Type de returns", options=["simple", "log"], index=0, key="dist_return_type")
                    nbins = st.number_input("Nombre de bins", min_value=10, max_value=1000, value=300, step=10, key="dist_nbins")
                    
                    st.markdown("### Evolution du cours")
                    days_evol = st.slider("Nombre de jours d'évolution à afficher",
                                          min_value=1, 
                                          max_value=len(hist_data), 
                                          value=min(252, len(hist_data)))
                    moving_averages = st.multiselect("Sélectionnez les moyennes mobiles à afficher", 
                                                     options=["MA20", "MA50", "MA100"],
                                                     default=["MA20"])
                    
                    submit_all = st.form_submit_button("Mettre à jour les graphiques")
                    
                    if submit_all:
                        # Graphique 1 : Distribution des returns
                        filtered_data = hist_data.tail(days_dist)
                        returns = compute_returns(filtered_data)
                        fig1 = plot_return_distribution(returns, nbins=nbins, return_type=return_type)
                        st.plotly_chart(fig1, use_container_width=True)
                        
                        st.divider()
                        # Graphique 2 : Evolution du cours
                        evolution_data = hist_data.tail(days_evol).copy()
                        x_axis = evolution_data['Date'] if 'Date' in evolution_data.columns else evolution_data.index
                        fig2 = px.line(evolution_data, x=x_axis, y='Close', 
                                       title=f"Evolution du cours sur les {days_evol} derniers jours")
                        # Ajout des moyennes mobiles sélectionnées
                        if "MA20" in moving_averages:
                            evolution_data["MA20"] = evolution_data["Close"].rolling(window=20).mean()
                            fig2.add_scatter(x=x_axis, y=evolution_data["MA20"], mode="lines", name="MA20")
                        if "MA50" in moving_averages:
                            evolution_data["MA50"] = evolution_data["Close"].rolling(window=50).mean()
                            fig2.add_scatter(x=x_axis, y=evolution_data["MA50"], mode="lines", name="MA50")
                        if "MA100" in moving_averages:
                            evolution_data["MA100"] = evolution_data["Close"].rolling(window=100).mean()
                            fig2.add_scatter(x=x_axis, y=evolution_data["MA100"], mode="lines", name="MA100")
                        st.plotly_chart(fig2, use_container_width=True)
                
                # Bouton pour ajouter l'actif au portefeuille
                if st.button("Ajouter cet actif au portefeuille", key="add_to_portfolio_button"):
                    # Initialiser le dictionnaire assets dans session_state si inexistant
                    if 'assets' not in st.session_state:
                        st.session_state.assets = {}
                    st.session_state.assets[ticker_selected] = {
                        "nom": asset_name,
                        "df": hist_data,
                        "quantity": 0
                    }
                    st.success(f"L'actif {ticker_selected} a été ajouté au portefeuille")
            else:
                st.write(f"Aucune donnée trouvée pour le ticker : {ticker_selected}")


def show_stock_informations():
    if 'resultats' in st.session_state:
        st.divider()
        st.write("### Liste des resultats les plus pertinents:")
        st.dataframe(st.session_state['resultats'], width=1000)
        
        # Création d'une liste d'options pour le sélecteur
        options = st.session_state['resultats'].apply(lambda row: f"{row['Ticker']} - {row['Name']}", axis=1).tolist()
        st.selectbox("Sélectionnez l'actif qui vous intéresse :", options, key="selected_asset")
        
        # Affichage des informations historiques si le bouton est cliqué ou si déjà affiché
        if st.button("Afficher les informations historiques") or st.session_state.get("display_history", False):
            st.session_state.display_history = True
            
            # Extraction du ticker et du nom depuis la sélection (format "TICKER - Name")
            ticker_selected = st.session_state.selected_asset.split(" - ")[0]
            asset_name = st.session_state.selected_asset.split(" - ")[1] if " - " in st.session_state.selected_asset else ticker_selected
            
            st.markdown(f"## Informations fondamentales pour **{ticker_selected}**")
            fundamental_info = get_fundamental_info(ticker_selected)
            
            # Affichage des informations fondamentales dans des expandeurs
            for key, value in fundamental_info.items():
                with st.expander(f"{key}", expanded=True):
                    if key == "Capitalisation boursière":
                        formatted_value = f"<span style='color:green'>{format(int(value), ',')} $</span>"
                        st.markdown(formatted_value, unsafe_allow_html=True)
                    else:
                        st.write(value)
            
            st.divider()
            hist_data = tickerf(ticker_selected)
            if hist_data is not None:
                st.markdown(f"## Historique du cours pour **{ticker_selected}**")
                st.dataframe(hist_data)
                
                st.markdown("## Paramètres des graphiques")
                # Formulaire global pour les deux graphiques
                with st.form(key="all_graphs"):
                    st.markdown("### Distribution des returns")
                    days_dist = st.slider("Nombre de jours à prendre en compte (distribution)",
                                          min_value=1, 
                                          max_value=len(hist_data), 
                                          value=min(252, len(hist_data)))
                    return_type = st.radio("Type de returns", options=["simple", "log"], index=0, key="dist_return_type")
                    nbins = st.number_input("Nombre de bins", min_value=10, max_value=1000, value=300, step=10, key="dist_nbins")
                    
                    st.markdown("### Evolution du cours")
                    days_evol = st.slider("Nombre de jours d'évolution à afficher",
                                          min_value=1, 
                                          max_value=len(hist_data), 
                                          value=min(252, len(hist_data)))
                    moving_averages = st.multiselect("Sélectionnez les moyennes mobiles à afficher", 
                                                     options=["MA20", "MA50", "MA100"],
                                                     default=["MA20"])
                    
                    submit_all = st.form_submit_button("Mettre à jour les graphiques")
                    
                    if submit_all:
                        # Graphique 1 : Distribution des returns
                        filtered_data = hist_data.tail(days_dist)
                        returns = compute_returns(filtered_data)
                        fig1 = plot_return_distribution(returns, nbins=nbins, return_type=return_type)
                        st.plotly_chart(fig1, use_container_width=True)
                        
                        st.divider()
                        # Graphique 2 : Evolution du cours
                        evolution_data = hist_data.tail(days_evol).copy()
                        x_axis = evolution_data['Date'] if 'Date' in evolution_data.columns else evolution_data.index
                        fig2 = px.line(evolution_data, x=x_axis, y='Close', 
                                       title=f"Evolution du cours sur les {days_evol} derniers jours")
                        # Ajout des moyennes mobiles sélectionnées
                        if "MA20" in moving_averages:
                            evolution_data["MA20"] = evolution_data["Close"].rolling(window=20).mean()
                            fig2.add_scatter(x=x_axis, y=evolution_data["MA20"], mode="lines", name="MA20")
                        if "MA50" in moving_averages:
                            evolution_data["MA50"] = evolution_data["Close"].rolling(window=50).mean()
                            fig2.add_scatter(x=x_axis, y=evolution_data["MA50"], mode="lines", name="MA50")
                        if "MA100" in moving_averages:
                            evolution_data["MA100"] = evolution_data["Close"].rolling(window=100).mean()
                            fig2.add_scatter(x=x_axis, y=evolution_data["MA100"], mode="lines", name="MA100")
                        st.plotly_chart(fig2, use_container_width=True)
                
                # Bouton pour ajouter l'actif au portefeuille
                if st.button("Ajouter cet actif au portefeuille", key="add_to_portfolio_button"):
                    # Initialiser le dictionnaire assets dans session_state si inexistant
                    if 'assets' not in st.session_state:
                        st.session_state.assets = {}
                    st.session_state.assets[ticker_selected] = {
                        "nom": asset_name,
                        "df": hist_data,
                        "quantity": 0
                    }
                    st.success(f"L'actif {ticker_selected} a été ajouté au portefeuille")
            else:
                st.write(f"Aucune donnée trouvée pour le ticker : {ticker_selected}")

