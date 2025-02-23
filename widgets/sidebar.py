import streamlit as st

def sidebar_widgets():
    st.sidebar.title("Menu latéral")
    st.sidebar.write("Widgets factices pour le moment :")
    
    # Exemple de slider
    dummy_slider = st.sidebar.slider("Slider factice", min_value=0, max_value=100, value=50)
    
    # Exemple de sélecteur
    dummy_select = st.sidebar.selectbox("Sélection factice", options=["Option 1", "Option 2", "Option 3"])
    
    # Exemple de checkbox
    dummy_checkbox = st.sidebar.checkbox("Case à cocher factice")
    
    # Ces widgets n'ont pour l'instant aucun effet fonctionnel.
    st.sidebar.write("Valeur du slider :", dummy_slider)
    st.sidebar.write("Option sélectionnée :", dummy_select)
    st.sidebar.write("Checkbox activée :", dummy_checkbox)