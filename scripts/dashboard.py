import streamlit as st
import plotly.graph_objects as go
import json

def load_data():
    try:
        with open("data/transactions.json") as f:
            return json.load(f)
    except:
        return []

def show_dashboard():

    st.markdown("# 💰 Dashboard")

    data = load_data()

    income = sum(t["amount"] for t in data if t["type"] == "income")
    expense = sum(t["amount"] for t in data if t["type"] == "expense")
    balance = income - expense

    # 🎨 CSS ULTRA PRO
    st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
    }

    .card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        padding: 25px;
        border-radius: 18px;
        color: white;
        box-shadow: 0px 8px 25px rgba(0,0,0,0.4);
        transition: 0.3s;
    }

    .card:hover {
        transform: scale(1.03);
    }

    .title {
        font-size: 14px;
        color: #94a3b8;
    }

    .value {
        font-size: 32px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    st.write("")

    # 🧱 CARTES
    col1, col2, col3 = st.columns(3)

    col1.markdown(f"""
    <div class="card">
        <div class="title">💰 Solde total</div>
        <div class="value">{balance} FCFA</div>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
    <div class="card">
        <div class="title">📈 Revenus</div>
        <div class="value">{income} FCFA</div>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
    <div class="card">
        <div class="title">📉 Dépenses</div>
        <div class="value">{expense} FCFA</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # 📊 GRAPHIQUE PRO
    dates = [t["date"] for t in data]
    values = [t["amount"] if t["type"]=="income" else -t["amount"] for t in data]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates,
        y=values,
        mode="lines+markers",
        line=dict(width=4),
        name="Flux"
    ))

    fig.update_layout(
        template="plotly_dark",
        height=400,
        margin=dict(l=10, r=10, t=30, b=10)
    )

    st.plotly_chart(fig, use_container_width=True)