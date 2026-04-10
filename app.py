import streamlit as st
from scripts.auth import login, register
from scripts.accounts import add_transaction, calculate_balances
from scripts.dashboard import show_dashboard
from scripts.projects import project_alerts
from scripts.forecast import forecast
from scripts.auth import is_premium
from scripts.history import show_history

st.set_page_config(
    page_title="Finance SaaS",
    page_icon="💼",
    layout="wide"
)

def card(title, value):
    st.markdown(f"""
        <div style="
            background-color:#1A1D23;
            padding:20px;
            border-radius:10px;
            box-shadow:0 0 10px rgba(0,0,0,0.3);
            text-align:center;">
            <h4>{title}</h4>
            <h2>{value}</h2>
        </div>
    """, unsafe_allow_html=True)

# SESSION
if "user" not in st.session_state:
    st.session_state.user = None

# LOGIN / REGISTER
if st.session_state.user is None:

    st.title("🔐 Connexion")

    choice = st.selectbox("Choisir", ["Login", "Register"])

    username = st.text_input("Nom utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if choice == "Login":
        if st.button("Se connecter"):
            if login(username, password):
                st.session_state.user = username
                st.success("Connecté !")
            else:
                st.error("Identifiants incorrects")

    else:
        if st.button("Créer compte"):
            if register(username, password):
                st.success("Compte créé !")
            else:
                st.error("Utilisateur existe déjà")

    st.stop()

# APP PRINCIPALE
username = st.session_state.user

st.sidebar.markdown("## Finance SaaS")
st.sidebar.write("---")


menu = st.sidebar.radio(
    "Navigation",
    ["Ajouter transaction", "Voir solde", "Dashboard", "Alertes", "Prévisions", "Historique", "Premium"]
)

st.sidebar.write("---")
st.sidebar.success(f"Connecté : {st.session_state.user}")

# AJOUT TRANSACTION
if menu == "Ajouter transaction":

    st.title("➕ Ajouter une transaction")

    amount = st.number_input("Montant", min_value=0.0)
    type_ = st.selectbox("Type", ["income", "expense"])
    project = st.text_input("Projet")

    if st.button("Ajouter"):
        add_transaction(username, amount, type_, project)
        st.success("Transaction ajoutée !")

# SOLDE
elif menu == "Voir solde":

    st.title("💰 Solde")

    balance = calculate_balances(username)

    st.metric("Solde actuel", balance)

# DASHBOARD
elif menu == "Dashboard":

    show_dashboard()

# ALERTES
elif menu == "Alertes":

    project_alerts()

if menu == "Prévisions":
    forecast() 

elif menu == "📈 Prévisions":

    if not is_premium(username):
        st.error("🔒 Réservé aux utilisateurs Premium")
        st.info("Va dans 💳 Premium pour activer ton accès")
    else:
        forecast()  

elif menu == "Historique":
    show_history()          

elif menu == "💳 Premium":

    st.title("💳 Abonnement Premium")

    st.write("### 🚀 Passe au plan Premium")

    st.write("""
    ✔ Transactions illimitées  
    ✔ Prévisions avancées 📈  
    ✔ Dashboard complet  
    ✔ Alertes intelligentes  
    """)

    st.write("---")

    st.subheader("🎁 Offre actuelle")
    st.success("1er mois GRATUIT")

    st.write("---")

st.subheader("💰 Paiement")

st.info("📱 Orange Money : +226 67 45 45 91")
st.info("📱 Moov Money : +226 70 30 44 10")

st.warning("⚠️ Après paiement, envoyez une preuve pour activation")

st.success("📞 WhatsApp : +226 55 46 57 62")        