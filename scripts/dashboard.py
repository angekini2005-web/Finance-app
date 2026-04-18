import streamlit as st
import plotly.graph_objects as go
import json
import pandas as pd

# 📂 Charger données
def load_data():
    try:
        with open("data/transactions.json") as f:
            return json.load(f)
    except:
        return []

def show_dashboard():

    st.set_page_config(layout="wide")

    data = load_data()

    income = sum(t["amount"] for t in data if t["type"] == "income")
    expense = sum(t["amount"] for t in data if t["type"] == "expense")
    balance = income - expense

    # 🎨 STYLE GLOBAL (CORRIGÉ + LISIBLE)
    st.markdown("""
    <style>

    /* 🌍 Fond */
    [data-testid="stAppViewContainer"] {
        background-color: #f5f7fb;
    }

    /* 📌 Sidebar premium */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* 🧱 Cartes */
    .card {
        background: white;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    /* 📝 TITRES (FIX ICI) */
    h1, h2, h3, h4 {
        color: #111827 !important;
    }

    .metric-title {
        font-size: 13px;
        color: #6b7280;
    }

    .metric-value {
        font-size: 26px;
        font-weight: 600;
        color: #111827;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .badge-green {
        background: #22c55e;
        color: white;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 11px;
    }

    .badge-red {
        background: #ef4444;
        color: white;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 11px;
    }

    </style>
    """, unsafe_allow_html=True)

    # 📌 SIDEBAR PRO
    st.sidebar.title("💼 Finance App")
    st.sidebar.markdown("---")
    st.sidebar.markdown("🏠 Dashboard")
    st.sidebar.markdown("🚨 Alertes")
    st.sidebar.markdown("📊 Prévisions")
    st.sidebar.markdown("📄 Historique")
    st.sidebar.markdown("---")
    st.sidebar.info("Version Premium 🔒")

    # 🏷️ TITRE PRINCIPAL
    st.markdown("## 💰 Dashboard Financier")

    # 🧠 BADGE
    badge_class = "badge-green" if balance >= 0 else "badge-red"
    badge_value = "+5%" if balance >= 0 else "-5%"

    # 🧱 CARTES
    col1, col2, col3 = st.columns(3)

    col1.markdown(f"""
    <div class="card">
        <div class="metric-title">Solde total</div>
        <div class="metric-value">
            {balance} FCFA
            <span class="{badge_class}">{badge_value}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
    <div class="card">
        <div class="metric-title">Revenus</div>
        <div class="metric-value">
            {income} FCFA
            <span class="badge-green">+12%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
    <div class="card">
        <div class="metric-title">Dépenses</div>
        <div class="metric-value">
            {expense} FCFA
            <span class="badge-red">-3%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # 📊 + 📋 LAYOUT
    left, right = st.columns([2,1])

    # 📊 GRAPHIQUE
    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📈 Évolution financière")

        if data:
            dates = [t["date"] for t in data]
            revenus = [t["amount"] if t["type"]=="income" else 0 for t in data]
            depenses = [t["amount"] if t["type"]=="expense" else 0 for t in data]

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=dates,
                y=revenus,
                mode="lines",
                name="Revenus",
                line=dict(width=2)
            ))

            fig.add_trace(go.Scatter(
                x=dates,
                y=depenses,
                mode="lines",
                name="Dépenses",
                line=dict(width=2)
            ))

            fig.update_layout(
                template="plotly_white",
                height=320,
                margin=dict(l=0, r=0, t=10, b=0)
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée")

        st.markdown('</div>', unsafe_allow_html=True)

    # 📋 TABLEAU
    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📄 Transactions")

        if data:
            df = pd.DataFrame(data).tail(5)

            df["Montant"] = df.apply(
                lambda x: f"+{x['amount']} FCFA" if x["type"] == "income"
                else f"-{x['amount']} FCFA",
                axis=1
            )

            df = df.rename(columns={
                "date": "Date",
                "type": "Type"
            })

            df = df[["Date", "Type", "Montant"]]

            st.dataframe(df, use_container_width=True)
        else:
            st.info("Aucune transaction")

        st.markdown('</div>', unsafe_allow_html=True)