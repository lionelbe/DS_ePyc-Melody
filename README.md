> This project is in french.<br>
> It was done during our training of Data Scientist at DataScientest (august 2021 - june 2022). <br>
> The aim was to put into practice the skills acquired during the training.<br>
> We sought to build a system of recommendations based on user data on twitter.


# :speaker: ePyc-Melody :musical_note:

Ce projet fait partie de la formation  [Datascientest.com](https://datascientest.com/) (cursus Data Scientist d'aout 2021).
![Datascientest_logo](/ressources/datascientest768x130.png)


:warning: Les datasets sont bien trop gros pour être déposés sur github ou sur google collab.<br>
Il est possible de les récupérer sur kaggle :
https://www.kaggle.com/chelseapower/nowplayingrs
1. context_content_features.csv ( 2,19Go )
2. sentiment_values.csv ( 373Ko )
3. user_track_hashtag_timestamp.csv ( 1,22Go )

## :dart: Objectif :dart:

Le titre et la description du projet permettaient au moins deux interprétations :
- Titre : Recommandations musicales – Prédire les musiques les plus appréciées sur Twitter.

- Description : Prédire si une musique sera plus ou moins appréciée à partir d’analyses et retours Twitter.

La description nous a incité à voir s'il était possible de prédire si un morceau de musique serait plus ou moins apprécié en se basant par exemple sur les  dictionnaires de sentiments présents dans les datasets, la popularité du morceau, ... 
C'est notre première approche, notre modèle n°1.

Le titre "Recommandations musicales" nous a emmené vers une autre approche basée sur un système de recommandation.
Pour ce faire nous avons testé deux méthodes : le clustering des spécificités musicales (modèle n°2), et la vectorisation des hashtags (modèle n°3).

## :bookmark_tabs: Description des fichiers :bookmark_tabs:
- ePycMelody_00_dataviz.ipynb <br>Dataviz et constitution du fichier de travail df_global.csv
- ePycMelody_01_modele0-sentiments.ipynb <br>Recherche d'un modèle basé sur les dictionnaires de sentiment et/ou la popularité.<br>(modèle abandonné)
- ePycMelody_02_modele1-clustering.ipynb <br>Modèle n°1 : Recommandations par clustering sur les caractéristiques musicales.
- ePycMelody_03_modele2-vectorisation.ipynb <br>Modèle n°2 : Recommandations par vectorisation des hashtags.

## :video_game: Demo streamlit  :video_game:
Pour tester l'application streamlit :
```shell
cd streamlit
conda create --name epycMelody python=3.9
conda activate epycMelody
pip install -r requirements.txt
streamlit run app.py
```

## :computer: Credits :computer:

*	Lionel BERENGER [(LinkedIn)](https://www.linkedin.com/in/lionelberenger/)
*	Nicolas FREYCHET [(LinkedIn)](https://www.linkedin.com/in/nicolas-freychet-1531391b9/)

Mentor :
*	Frédéric FRANCINE 

![Projet_logo](/ressources/logo_white1.jpg)
