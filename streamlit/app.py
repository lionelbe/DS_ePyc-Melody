import streamlit as st

from collections import OrderedDict
from pathlib import Path

# PATH = Path(__file__).parents[1]
PATH = "./" # local


if 'PATH' not in st.session_state:
    st.session_state['PATH'] = PATH

# TITLE, TEAM_MEMBERS and PROMOTION
import config

# PAGES
from tabs import intro, clusters, vector

# CONFIG

st.set_page_config(
    page_title=config.TITLE,
    page_icon="https://datascientest.com/wp-content/uploads/2020/03/cropped-favicon-datascientest-1-32x32.png",
)

with open("style.css", "r") as f:
    style = f.read()

st.markdown(f"<style>{style}</style>", unsafe_allow_html=True)


# PAGES / MENU
TABS = OrderedDict(
    [
        (intro.sidebar_name, intro),
        (clusters.sidebar_name, clusters),
        (vector.sidebar_name, vector),
    ]
)

def run():
    st.sidebar.image(st.session_state.PATH+"assets/logo_rapport.jpg", width=200)
    
    tab_name = st.sidebar.radio("", list(TABS.keys()), 0)
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"## {config.PROMOTION}", unsafe_allow_html=True)

    st.sidebar.markdown("### Equipe :")
    for member in config.TEAM_MEMBERS:
        st.sidebar.markdown(member.sidebar_markdown(), unsafe_allow_html=True)

    st.sidebar.markdown("### Chef de cohorte :")
    st.sidebar.markdown("#### Frédéric Francine")

    st.sidebar.image(st.session_state.PATH+"assets/datascientest150x25.png", width=150)


    tab = TABS[tab_name]

    tab.run()


if __name__ == "__main__":
    run()
