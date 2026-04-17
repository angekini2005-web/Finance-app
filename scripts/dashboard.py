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

    st.title("💰 Dashboard Financier")

    data = load_data()

    income = sum(t["amount"] for t in data if t["type"] == "income")
    expense = sum(t["amount"] for t in data if t["type"] == "expense")
    balance = income - expense

    # 🎨 STYLE GLOBAL (BLANC + PRO)
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
    }

    .badge-red {
        background-color: #ef4444;
        color: white;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

    # 📊 CALCUL POUR BADGE
    if balance >= 0:
        badge = f"<span class='badge-green'>+5%</span>"
    else:
        badge = f"<span class='badge-red'>-5%</span>"

    # 🧱 CARTES
    col1, col2, col3 = st.columns(3)

    col1.markdown(f"""
    <div class="card">
        <div class="metric-title">Solde total</div>
        <div class="metric-value">{balance} FCFA {badge}</div>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
    <div class="card">
        <div class="metric-title">Revenus</div>
        <div class="metric-value">{income} FCFA <span class='badge-green'>+12%</span></div>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
    <div class="card">
        <div class="metric-title">Dépenses</div>
        <div class="metric-value">{expense} FCFA <span class='badge-red'>-3%</span></div>
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
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")

    # 📋 TABLEAU
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📄 Dernières transactions")

    if data:
        df = pd.DataFrame(data).tail(5)

        def color(val):
            if isinstance(val, (int, float)):
                return "color: green" if val > 0 else "color: red"
            return ""

        st.dataframe(df.style.applymap(color, subset=["amount"]),
                     use_container_width=True)
    else:
        st.info("Aucune transaction")

    st.markdown('</div>', unsafe_allow_html=True)