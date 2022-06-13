"""

Config file for Streamlit App

"""
import streamlit as st
from member import Member

TITLE = "ePyc melody"

TEAM_MEMBERS = [
    Member(
        name="Lionel Bérenger",
        linkedin_url="https://www.linkedin.com/in/lionelberenger/"
    ),
    Member(
        name="Nicolas Freychet",
        linkedin_url="https://www.linkedin.com/in/nicolas-freychet/"
    )
]

PROMOTION = "Formation continue <br>Data Scientist<br> Aout 2021"
