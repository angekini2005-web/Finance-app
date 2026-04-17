import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import json

def load_data():
    try:
        with open("data/transactions.json") as f:
            return json.load(f)
    except:
        return []

def show_dashboard():
    st.title("💰 Dashboard Financier")

    data = load_data()

    income = sum(t["amount"] for t in data if t["type"] == "income")
    expense = sum(t["amount"] for t in data if t["type"] == "expense")
    balance = income - expense

    # 🎨 CSS
    st.markdown("""
    <style>
    .card {
        background-color: #111827;
        padding: 20px;
        border-radius: 15px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    col1.markdown(f"<div class='card'>💰 Solde<br><h2>{balance}$</h2></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='card'>📈 Revenus<br><h2>{income}$</h2></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='card'>📉 Dépenses<br><h2>{expense}$</h2></div>", unsafe_allow_html=True)

    # 📊 Graphique
    dates = [t["date"] for t in data]
    amounts = [t["amount"] if t["type"]=="income" else -t["amount"] for t in data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=amounts, mode="lines+markers"))

    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)