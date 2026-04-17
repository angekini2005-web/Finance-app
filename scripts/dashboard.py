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

    st.markdown("## 💰 Financial Dashboard")

    data = load_data()

    # 📊 Calculs
    income = sum(t["amount"] for t in data if t["type"] == "income")
    expense = sum(t["amount"] for t in data if t["type"] == "expense")
    balance = income - expense

    # 🧠 LOGIQUE GAIN / PERTE
    if balance > 0:
        status_text = f"🟢 Surplus: +{balance} FCFA"
        status_color = "#22c55e"
    elif balance < 0:
        status_text = f"🔴 Perte: {balance} FCFA"
        status_color = "#ef4444"
    else:
        status_text = "⚖️ Équilibre"
        status_color = "#9ca3af"

    # 🎨 STYLE GLOBAL
    st.markdown(f"""
    <style>
    .main {{
        background-color: #0f172a;
    }}

    .card {{
        background: #111827;
        padding: 20px;
        border-radius: 15px;
        color: white;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }}

    .title {{
        font-size: 14px;
        color: #9CA3AF;
    }}

    .value {{
        font-size: 28px;
        font-weight: bold;
    }}

    .status {{
        font-size: 14px;
        color: {status_color};
        margin-top: 5px;
    }}
    </style>
    """, unsafe_allow_html=True)

    # 🧱 CARTES KPI
    col1, col2, col3 = st.columns(3)

    col1.markdown(f"""
    <div class="card">
        <div class="title">Total Balance</div>
        <div class="value">{balance} FCFA</div>
        <div class="status">{status_text}</div>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
    <div class="card">
        <div class="title">Income</div>
        <div class="value">{income} FCFA</div>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
    <div class="card">
        <div class="title">Expenses</div>
        <div class="value">{expense} FCFA</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # 📊 + 📋 LAYOUT PRINCIPAL
    left, right = st.columns([2, 1])

    # 📊 GRAPHIQUE
    with left:
        st.subheader("📊 Cash Flow")

        if data:
            dates = [t["date"] for t in data]
            values = [
                t["amount"] if t["type"] == "income" else -t["amount"]
                for t in data
            ]

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=dates,
                y=values,
                mode="lines+markers",
                line=dict(width=3),
                name="Flux"
            ))

            fig.update_layout(
                template="plotly_dark",
                height=400,
                margin=dict(l=10, r=10, t=30, b=10)
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée disponible")

    # 📋 TABLEAU À DROITE
    with right:
        st.subheader("📋 Transactions récentes")

        if data:
            df = pd.DataFrame(data)

            # dernières transactions
            df = df.tail(5)

            st.dataframe(df, use_container_width=True)
        else:
            st.info("Aucune transaction")