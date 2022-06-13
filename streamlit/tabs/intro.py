import streamlit as st
import pandas as pd

title = "<h1>Introduction</h1>"
sidebar_name = "Introduction"

@st.cache
def get_data():
    df_eval = pd.read_csv(st.session_state.PATH+"data/data_streamlit_evaluation.csv",index_col=0) #only tracks associated with specific music genre
    return df_eval


def run():

    # titre
    st.markdown(title, unsafe_allow_html=True)

    # contenu

    
    st.markdown("Ce projet fait partie de la formation <a href='https://datascientest.com/' target='blank'>Datascientest.com</a> (formation continue, session aout 2021).<br/> Le projet consiste à bâtir un système de recommandations musicales basée sur des données twitter.", unsafe_allow_html=True)
    st.markdown("Les datasets originaux sont disponibles sur <a href='https://www.kaggle.com/chelseapower/nowplayingrs' target='blank'>Kaggle</a> : <ul><li><b>context_content_features.csv</b> ( 2,19Go )<br/>22 variables et 11 614 671 entrées</li><li><b>sentiment_values.csv</b> ( 373Ko )<br/>21 variables et 5290 entrées</li><li><b>user_track_hashtag_timestamp.csv</b> ( 1,22Go )<br/>4 variables et 17 560 113 entrées</li></ul>", unsafe_allow_html=True)
    
    st.markdown("<b>Ces jeux de données ont été analysés et retravaillés</b> (cf <a href='https://github.com/DataScientest-Studio/ePyc-Melody/raw/main/documents/Rapport_ePyc-melody.pdf' target='blank'>rapport</a>).<br/> A partir de là, un dataset de travail a été créé, il a servi à l'entrainement des modèles.<br/> Le détail des travaux est visible sur <a href='https://github.com/DataScientest-Studio/ePyc-Melody/' target='blank'>github (jupyter notebooks)</a>", unsafe_allow_html=True)
    st.markdown("<b>Un rapport (disponible sur github) détaille les étapes du projet</b> : <a href='https://github.com/DataScientest-Studio/ePyc-Melody/raw/main/documents/Rapport_ePyc-melody.pdf' target='blank'>télécharger le rapport</a>", unsafe_allow_html=True)

    
    st.markdown("<h4/>Ici, nous ne présentons que les modèles ayant aboutis</h4><b>C'est à dire les systèmes de recommandations basés sur les caractéristiques musicales et lexicales.</b>", unsafe_allow_html=True)
    st.markdown("Le fichier utilisé pour le clustering est un fichier épuré et ré-équilibré, avec 100 chansons pour chaque style musical :")
    
    df_eval = get_data()

    if st.checkbox("Afficher un apercu des données"):
        st.write("Chaque piste est définie par plusieurs caractéristiques musicales et un ou plusieurs styles musicaux.") 
        st.dataframe(df_eval.head())

    if st.checkbox("Afficher les différents genres"):
        st.write(df_eval['hashtag'].unique())
    