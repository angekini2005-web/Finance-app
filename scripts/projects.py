import streamlit as st
from scripts.accounts import load_transactions

def project_alerts():

    username = st.session_state.user
    transactions = load_transactions(username)

    if not transactions:
        st.warning("❌ Aucune transaction")
        return

    project_data = {}

    for t in transactions:
        project = t.get("project")

        if not project:
            continue

        if project not in project_data:
            project_data[project] = 0

        if t["type"] == "income":
            project_data[project] += t["amount"]
        else:
            project_data[project] -= t["amount"]

    st.title("🚨 Alertes projets")

    for project, balance in project_data.items():

        st.subheader(f"📁 {project}")

        if balance < 0:
            st.error("🔴 Projet en perte")
        elif balance < 100:
            st.warning("⚠️ Projet faible")
        else:
            st.success("🟢 Projet rentable")

        st.write(f"💰 Solde : {balance}")
        st.write("---")