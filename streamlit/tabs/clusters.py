import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px


from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from wordcloud import WordCloud

title = "<h1>Modelisation <br/> clustering avec k-means</h1>"
sidebar_name = "Modélisation Clusters"


@st.cache
def get_data():
    ## Files to load:
    df = pd.read_csv(st.session_state.PATH+"data/data_streamlit_training.csv",index_col=0) #all track available
    df_eval = pd.read_csv(st.session_state.PATH+"data/data_streamlit_evaluation.csv",index_col=0) #only tracks associated with specific music genre
    #global list_trackid_evaluate
    list_trackid_evaluate = df_eval['track_id']
    ## scaler
    scaler = StandardScaler()
    scaler.fit(df)
    df[['instrumentalness','liveness','speechiness','danceability','valence','loudness','tempo','acousticness','energy']] = scaler.transform(df[['instrumentalness','liveness','speechiness','danceability','valence','loudness','tempo','acousticness','energy']])
    # Or if we want to train the model on filtered data:
    data_evaluate_features = scaler.transform(df_eval.drop(['track_id','hashtag'], axis=1))
    return df_eval, data_evaluate_features, list_trackid_evaluate

@st.cache
def run_model(data_evaluate_features, n_class):
    # model
    kmeans=KMeans(n_clusters=n_class, random_state=1234)
    kmeans.fit(data_evaluate_features)

    # Centroids and labels
    labels_kmeans = kmeans.labels_
    centroids_kmeans = kmeans.cluster_centers_
    model_ready=True
    return kmeans, labels_kmeans, centroids_kmeans, model_ready


def run():
    # titre
    st.markdown(title, unsafe_allow_html=True)

    #number of classes chosen
    n_class = 0
    n_class_new=4
    model_ready=False
    
    df_eval, data_evaluate_features, list_trackid_evaluate = get_data()

    # contenu
    txt = "Aperçu du jeu de données ("+str(df_eval.shape[0])+" entrées )"

    choix = st.radio(txt, ('head()', 'random(5)'))
    
    if (choix == 'head()'):
        st.dataframe(df_eval[['track_id', 'instrumentalness', 'speechiness', 'danceability', 'valence', 'loudness' ,'tempo', 'acousticness', 'energy']].head(), width=1200)
    else:
        st.dataframe(df_eval[['track_id', 'instrumentalness', 'speechiness', 'danceability', 'valence', 'loudness' ,'tempo', 'acousticness', 'energy']].sample(5), width=1200)
    


    st.markdown("<u>Clustering :</u>", unsafe_allow_html=True)

    n_class_new = st.slider("Choisissez un nombre de clusters:", min_value=4, max_value=16)
    if (n_class!=n_class_new):
        n_class=n_class_new
        runmodel=False
        model_ready=False
        
    # model (only run if not already run with the nb of class)
    kmeans, labels_kmeans, centroids_kmeans, model_ready = run_model(data_evaluate_features, n_class);
      
    if model_ready==True:
     st.write("Le modèle est prêt!")
    
     if st.checkbox("Afficher les clusters (PCA 2D) :"):
        pca = PCA(n_components=2);
        data_2D = pca.fit_transform(X=data_evaluate_features);
        fig_pca = plt.figure(figsize=(10,8))
        for label in np.unique(labels_kmeans):
            #lab=labels[label]
            lab=label
            plt.scatter(data_2D[labels_kmeans==label, 0], data_2D[labels_kmeans==label, 1], s=15-label, label=lab)
        # add mean of each group and std
        for label in np.unique(labels_kmeans):
            avg1=data_2D[labels_kmeans==label, 0].mean()
            avg2=data_2D[labels_kmeans==label, 1].mean()
            std1=data_2D[labels_kmeans==label, 0].std()
            std2=data_2D[labels_kmeans==label, 1].std()
            plt.vlines(x=avg1, ymin=avg2-std2, ymax=avg2+std2, colors='black', linestyles='-', lw=2, zorder=9)
            plt.hlines(y=avg2, xmin=avg1-std1, xmax=avg1+std1, colors='black', linestyles='-', lw=2, zorder=9)
            plt.scatter(avg1, avg2, s=100, edgecolors="black", facecolors='none', zorder=10)
        plt.xlabel('PCA 1');
        plt.ylabel('PCA 2');
        plt.title("Projection on two first PCA axes");
        plt.legend()
        st.pyplot(fig_pca)

     if st.checkbox("Afficher les clusters (PCA 3D) :"):
        model_pca3D = PCA(n_components=3);
        data_pca3D = model_pca3D.fit_transform(X=data_evaluate_features);

        df_3d = pd.DataFrame()
        for label in np.unique(labels_kmeans):
            tmp = { 'x' : data_pca3D[labels_kmeans==label, 0],
                'y' : data_pca3D[labels_kmeans==label, 1],
                'z' : data_pca3D[labels_kmeans==label, 2],
                'label' : str(label)
                }
            df_3d = pd.concat([df_3d, pd.DataFrame.from_dict(tmp)], ignore_index=True)

        fig = px.scatter_3d(df_3d, x='x', y='y', z='z', color='label')
            # color_discrete_sequence=np.unique(labels_kmeans), category_orders=np.unique(labels_kmeans))
        # fig.show()
        st.plotly_chart(fig)

     if st.checkbox("Afficher les WordClouds :"):       
        ### Affiche Wordcloud quand le modèle est prêt:
        st.write("Les {} groupes obtenus sont les suivants:".format(n_class))
        # prepare data evalution:
        labels_kmeans_evaluate = kmeans.predict(data_evaluate_features);
        list_trackid_evaluate = pd.DataFrame(list_trackid_evaluate)
        list_trackid_evaluate['labels'] = labels_kmeans_evaluate
        data_merge = pd.merge(df_eval, list_trackid_evaluate, on='track_id')[['track_id','hashtag','labels']];
        data_merge.drop_duplicates(inplace=True); #make sure only 1 same hashtag for a song
        #plt.figure(figsize=(15, 10))
        fig_pclass, axs = plt.subplots(1+n_class//4, 4, figsize=(16, 4*(1+n_class//4)))
        i=0;j=0;
        for n in range(0,n_class):
          #lab=labels[n]
          df_test = data_merge[data_merge['labels']==n][['hashtag','labels']]
          if df_test.size == 0:
            axs[i, j].set_title('Empty')
          else:
           wordcloud = WordCloud(background_color = 'white', max_words = 5, collocations=False).generate(' '.join(df_test['hashtag']))
           label=[]
           for key in wordcloud.words_:
            label.append(key)
           axs[i, j].imshow(wordcloud)
           if len(label)==1:
            axs[i, j].set_title('Group {}: {}'.format(n,label[0]))
           else:
            axs[i, j].set_title('Group {}: {} {}'.format(n,label[0],label[1]))
          axs[i, j].axis("off")
          j+=1;
          if (j==4):
                i+=1;
                j=0;
        # if needed, delete axis of last sub-plot        
        for l in range(j, 4):
          axs[i, l].axis("off")  
        #plt.gcf().text(0.5, 1, 'Wordclouds for {} groups of music'.format(n_class), fontsize=18, horizontalalignment='center', verticalalignment='center') ;
        plt.tight_layout();
        st.pyplot(fig_pclass)
