import streamlit as st
from data.data_loader import tickerf, get_fundamental_info
from utilities.graphs_plots import plot_return_distribution
from utilities.base_tools import compute_returns


def show_stock_informations():
    # Si des résultats ont été stockés, les afficher
    if 'resultats' in st.session_state:
        st.divider()
        st.write("### Liste des resultats les plus pertinents:")
        st.dataframe(st.session_state['resultats'], width=1000)
        
        # Création d'une liste de chaînes pour l'affichage dans le menu déroulant
        options = st.session_state['resultats'].apply(lambda row: f"{row['Ticker']} - {row['Name']}", axis=1).tolist()
        
        # Menu déroulant pour sélectionner l'actif avec une clé pour préserver l'état
        st.selectbox("Sélectionnez l'actif qui vous intéresse :", options, key="selected_asset")
        
        # Bouton pour activer la récupération des informations historiques et fondamentales
        if st.button("Afficher les informations historiques"):
            # Extraction du ticker à partir de la sélection (format "TICKER - Name")
            ticker_selected = st.session_state.selected_asset.split(" - ")[0]
            
            # Récupération et affichage des informations fondamentales
            st.markdown(f"## Informations fondamentales pour **{ticker_selected}**")
            fundamental_info = get_fundamental_info(ticker_selected)
            
            # Utilisation de containers pour chaque section d'information fondamentale
            for key, value in fundamental_info.items():
                print(key)
                st.markdown(f"### {key}")
                # Définir la hauteur du container en fonction du champ
                container_height = 150 if key == "Résumé de l'activité" else 60
                with st.container(height=container_height):
                    # Si le champ correspond à la capitalisation, formater le nombre en dollars et l'afficher en vert
                    if key == "Capitalisation boursière":
                        print(value)
                        formatted_value = f"<span style='color:green'>{format(int(value), ',')} $</span>"
                        st.markdown(formatted_value, unsafe_allow_html=True)
                    else:
                        st.write(value)
            
            st.divider()
            hist_data = tickerf(ticker_selected)
            if hist_data is not None:
                st.markdown(f"## Historique du cours pour **{ticker_selected}**")
                st.dataframe(hist_data)
                
                
                # Créer et afficher le graphique
                fig = plot_return_distribution(compute_returns(hist_data), nbins=300, return_type='simple')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write(f"Aucune donnée trouvée pour le ticker : {ticker_selected}")