import streamlit as st
import json

def load_data():
    try:
        with open("data/transactions.json") as f:
            return json.load(f)
    except:
        return []

def project_alerts():
    st.subheader("🚨 Alertes")

    data = load_data()

    total = sum(t["amount"] if t["type"]=="income" else -t["amount"] for t in data)

    if total < 0:
        st.error("⚠️ Solde négatif !")
    elif total < 500:
        st.warning("⚠️ Solde faible")
    else:
        st.success("✅ Situation stable")

def forecast():
    st.subheader("📊 Prévisions")

    data = load_data()

    total = sum(t["amount"] if t["type"]=="income" else -t["amount"] for t in data)

    prediction = total * 1.2

    st.info(f"Projection 30 jours : {prediction}$")