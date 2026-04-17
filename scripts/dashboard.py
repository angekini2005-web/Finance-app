import streamlit as st
import plotly.graph_objects as go
import json
import pandas as pd

def load_data():
    try:
        with open("data/transactions.json") as f:
            return json.load(f)
    except:
        return []

def show_dashboard():

    st.markdown("## 💰 Financial Dashboard")

    data = load_data()

    income = sum(t["amount"] for t in data if t["type"] == "income")
    expense = sum(t["amount"] for t in data if t["type"] == "expense")
    balance = income - expense

    # 🎨 STYLE
    st.markdown("""
    <style>
    .card {
        background: #111827;
        padding: 20px;
        border-radius: 15px;
        color: white;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    .title {
        font-size: 14px;
        color: #9CA3AF;
    }
    .value {
        font-size: 28px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    # 🧱 CARTES
    col1, col2, col3 = st.columns(3)

    col1.markdown(f"""
    <div class="card">
        <div class="title">Total Balance</div>
        <div class="value">{balance} FCFA</div>
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

    # 📊 + 📋 LAYOUT COMME IMAGE
    left, right = st.columns([2,1])

    # 📊 GRAPHIQUE
    with left:
        st.subheader("📊 Overview")

        dates = [t["date"] for t in data]
        values = [t["amount"] if t["type"]=="income" else -t["amount"] for t in data]

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=dates,
            y=values,
            mode="lines+markers",
            line=dict(width=3),
            name="Cash Flow"
        ))

        fig.update_layout(
            template="plotly_dark",
            height=400,
            margin=dict(l=10, r=10, t=30, b=10)
        )

        st.plotly_chart(fig, use_container_width=True)

    # 📋 TABLEAU À DROITE
    with right:
        st.subheader("📋 Transactions")

        if data:
            df = pd.DataFrame(data)
            st.dataframe(df.tail(5), use_container_width=True)
        else:
            st.info("No data")