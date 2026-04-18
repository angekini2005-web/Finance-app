import streamlit as st
from scripts.dashboard import show_dashboard
from scripts.projects import project_alerts, forecast
from scripts.history import show_history
from scripts.auth import is_premium

st.set_page_config(page_title="Finance App", layout="wide")

username = st.sidebar.text_inpu("Nom utilisateur")

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

elif menu == "Prévisions":
    if is_premium(username):
        forecast()
    else:
        st.warning("🔒 Premium requis")

elif menu == "Premium":

    st.title("💳 Passer en Premium")

    st.write("Accès complet à l'application")

    st.markdown("### 💰 Paiement via Orange Money")
    st.markdown("Envoyez *3000 FCFA* au numéro : *67 45 45 91*")

    st.markdown("### 📲 Confirmation")
    st.markdown("Envoyez la preuve sur WhatsApp")

    st.markdown("[👉 Contacter sur WhatsApp](https://wa.me/22655465762)")            