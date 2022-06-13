import streamlit as st
import pandas as pd
import numpy as np
import pickle

from sklearn.metrics.pairwise import linear_kernel

title = "<h1>Recommandations <br/> basees sur les hashtags</h1>"
sidebar_name = "Recommandations hashtags"

model_ready = False
nb_reco = 5
recommandations=""
df_select_track = pd.read_csv(st.session_state.PATH+'data/df_vector_select_trackid.csv')
df_vector = pd.read_csv(st.session_state.PATH+'data/df_vector.csv')
tfidf = pickle.load(open(st.session_state.PATH+"data/tfidf_vector.pickle", "rb"))


# recherche de morceaux similaires via matrice vectorisée
@st.cache
def similar_tune(track_id, nb, df_vector, tfidf):
    # recherche de l'index du track_id dans le dataframe
    df_index = df_vector.index[df_vector['track_id']==track_id].tolist()[0]
    
    # matrice de similarité
    hashtag_similarities = linear_kernel(tfidf[df_index:df_index+1], tfidf).flatten()
    
    # resultats similaires (index)
    similar_tunes_idx = hashtag_similarities.argsort()[:-nb-1:-1]
    
    # conversion au format dataframe (index, track_id, hashtag)
    idx_fnd = []
    trk_fnd = []
    hsh_fnd = []
    
    for res in similar_tunes_idx:
        tune_found = df_vector.iloc[res]['track_id']
        hashtags_found = df_vector.iloc[res]['hashtag_cleaned']
        idx_fnd.append(res)
        trk_fnd.append(tune_found)
        hsh_fnd.append(hashtags_found)
    # return 
    model_ready = True
    recommandations = pd.DataFrame({'track_id' : trk_fnd,'hashtags' : hsh_fnd}) # 'idx' : idx_fnd,
    return recommandations, model_ready


## ------------------------------------------------------------------------------------------
## -
## -                                       MAIN
## -
## ------------------------------------------------------------------------------------------

def run():

    # titre
    st.markdown(title, unsafe_allow_html=True)

    # contenu
    txt = "Aperçu du jeu de données ("+str(df_vector.shape[0])+" entrées )"
    choix = st.radio(txt, ('head()', 'random(5)'))
    
    if (choix == 'head()'):
        st.dataframe(df_vector.head(), width=1200)
    else:
        st.dataframe(df_vector.sample(5), width=1200)

    

    st.markdown("<u>Recommandations :</u>", unsafe_allow_html=True)
    # selection de morceaux "triés"
    track_id = st.selectbox(
     'Selectionner un morceau',
     (df_select_track),
     key="track_id",
     format_func=lambda x: str(df_select_track[df_select_track['track_id']==x]['track_id'].values)[2:10]+"... - "+df_select_track[df_select_track['track_id']==x]['hashtag_cleaned'].values
     )


    nb_reco = st.slider("Nombre de recommandations:", min_value=5, max_value=20)
   

    hashtags = df_vector[df_vector['track_id'] == track_id]['hashtag_cleaned'].tolist()

    st.write('Morceau sélectionné:', track_id)
    st.write('hashtags :', hashtags[0])

    recommandations, model_ready = similar_tune(track_id, nb_reco, df_vector, tfidf)

    if (model_ready == True):
        st.markdown("Recommandations :")
        st.dataframe(recommandations, height = 1000, width=1200)


