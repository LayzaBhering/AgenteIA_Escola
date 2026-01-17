import streamlit as st
from login import login_page
from main_app import main_app

st.set_page_config(
    page_title="EstudanteAI",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    main_app()
else:
    login_page()

