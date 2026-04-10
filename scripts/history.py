import streamlit as st
import pandas as pd
from scripts.accounts import load_transactions

def show_history():

    st.title("📜 Historique des transactions")

    username = st.session_state.get("user", None)

    if not username:
        st.error("Utilisateur non connecté")
        return

    transactions = load_transactions(username)

    if not transactions:
        st.warning("Aucune transaction trouvée")
        return

    # Convertir en DataFrame
    df = pd.DataFrame(transactions)

    # Formatage date
    df["date"] = pd.to_datetime(df["date"])

    # Trier par date (plus récent en haut)
    df = df.sort_values(by="date", ascending=False)

    # 💰 Filtre type
    type_filter = st.selectbox(
        "Filtrer par type",
        ["Tous", "income", "expense"]
    )

    if type_filter != "Tous":
        df = df[df["type"] == type_filter]

    # 🔍 Recherche
    search = st.text_input("Rechercher (description)")

    if search:
        df = df[df["description"].str.contains(search, case=False)]

    # 💱 Format montant
    df["amount"] = df["amount"].astype(float)

    # Affichage
    st.dataframe(df, use_container_width=True)

    # 📊 Résumé
    st.write("### 📊 Résumé")

    total_income = df[df["type"] == "income"]["amount"].sum()
    total_expense = df[df["type"] == "expense"]["amount"].sum()

    col1, col2 = st.columns(2)

    with col1:
        st.success(f"💰 Revenus : {total_income:.2f}")

    with col2:
        st.error(f"💸 Dépenses : {total_expense:.2f}")