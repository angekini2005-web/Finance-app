import streamlit as st
from scripts.dashboard import show_dashboard
from scripts.projects import project_alerts, forecast
from scripts.history import show_history
from scripts.auth import is_premium

st.set_page_config(page_title="Finance App", layout="wide")

menu = st.sidebar.selectbox("Navigation", [
    "Dashboard",
    "Alertes",
    "Prévisions",
    "Historique"
])

if menu == "Dashboard":
    show_dashboard()

elif menu == "Alertes":
    project_alerts()

elif menu == "Prévisions":
    if is_premium():
        forecast()
    else:
        st.warning("🔒 Premium requis")

elif menu == "Historique":
    show_history()