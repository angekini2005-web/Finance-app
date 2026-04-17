import streamlit as st
import plotly.graph_objects as go
import json
import pandas as pd

# 📂 Charger les données
def load_data():
    try:
        with open("data/transactions.json") as f:
            return json.load(f)
    except:
        return []

# 🚀 Dashboard principal
def show_dashboard():

    st.title("💰 Dashboard Financier")

    data = load_data()

    # 📊 Calculs
    income = sum(t["amount"] for t in data if t["type"] == "income")
    expense = sum(t["amount"] for t in data if t["type"] == "expense")
    balance = income - expense

    # 📊 BADGES (simulation pro)
    badge_balance = "+5%" if balance >= 0 else "-5%"
    badge_income = "+12%"
    badge_expense = "-3%"

    badge_balance_class = "badge-green" if balance >= 0 else "badge-red"

    # 🎨 STYLE GLOBAL
    st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
    }

    .card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    }

    .metric-title {
        color: #6b7280;
        font-size: 14px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: bold;
    }

    .badge-green {
        background-color: #22c55e;
        color: white;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 12px;
        margin-left: 10px;
    }

    .badge-red {
        background-color: #ef4444;
        color: white;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 12px;
        margin-left: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # 🧱 CARTES KPI
    col1, col2, col3 = st.columns(3)

    col1.markdown(f"""
    <div class="card">
        <div class="metric-title">Solde total</div>
        <div class="metric-value">
            {balance} FCFA 
            <span class="{badge_balance_class}">{badge_balance}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
    <div class="card">
        <div class="metric-title">Revenus</div>
        <div class="metric-value">
            {income} FCFA 
            <span class="badge-green">{badge_income}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
    <div class="card">
        <div class="metric-title">Dépenses</div>
        <div class="metric-value">
            {expense} FCFA 
            <span class="badge-red">{badge_expense}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # 📊 GRAPHIQUE DANS UNE CARD
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📈 Évolution financière")

    if data:
        dates = [t["date"] for t in data]
        revenus = [t["amount"] if t["type"]=="income" else 0 for t in data]
        depenses = [t["amount"] if t["type"]=="expense" else 0 for t in data]

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=dates,
            y=revenus,
            mode="lines+markers",
            name="Revenus"
        ))

        fig.add_trace(go.Scatter(
            x=dates,
            y=depenses,
            mode="lines+markers",
            name="Dépenses"
        ))

        fig.update_layout(
            template="plotly_white",
            height=400,
            margin=dict(l=10, r=10, t=30, b=10)
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée")

    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")

    # 📋 TABLEAU PRO
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📄 Dernières transactions")

    if data:
        df = pd.DataFrame(data).tail(5)

        # 🧠 Format pro (comme ton image)
        def format_amount(row):
            if row["type"] == "income":
                return f"+ {row['amount']} FCFA"
            else:
                return f"- {row['amount']} FCFA"

        df["Montant"] = df.apply(format_amount, axis=1)

        df = df.rename(columns={
            "date": "Date",
            "type": "Type"
        })

        df = df[["Date", "Type", "Montant"]]

        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aucune transaction")

    st.markdown('</div>', unsafe_allow_html=True)