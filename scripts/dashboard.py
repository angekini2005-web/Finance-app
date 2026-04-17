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

# 🚀 Dashboard
def show_dashboard():

    data = load_data()

    income = sum(t["amount"] for t in data if t["type"] == "income")
    expense = sum(t["amount"] for t in data if t["type"] == "expense")
    balance = income - expense

    # 🎨 STYLE GLOBAL ULTRA PRO
    st.markdown("""
    <style>

    /* 🌍 Fond global */
    [data-testid="stAppViewContainer"] {
        background-color: #f5f7fb;
    }

    /* 📌 Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111827;
    }

    /* 🧱 Cartes */
    .card {
        background: white;
        padding: 18px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }

    .metric-title {
        font-size: 13px;
        color: #6b7280;
    }

    .metric-value {
        font-size: 26px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .badge-green {
        background: #22c55e;
        color: white;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 11px;
    }

    .badge-red {
        background: #ef4444;
        color: white;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 11px;
    }

    /* 📋 Table */
    table {
        width: 100%;
        border-collapse: collapse;
    }

    th {
        text-align: left;
        color: #6b7280;
        font-size: 13px;
    }

    td {
        padding: 8px 0;
        font-size: 14px;
    }

    </style>
    """, unsafe_allow_html=True)

    st.title("💰 Dashboard Financier")

    # 🧠 BADGES
    badge_balance_class = "badge-green" if balance >= 0 else "badge-red"
    badge_balance_value = "+5%" if balance >= 0 else "-5%"

    # 🧱 CARTES
    col1, col2, col3 = st.columns(3)

    col1.markdown(f"""
    <div class="card">
        <div class="metric-title">Solde total</div>
        <div class="metric-value">
            {balance} FCFA
            <span class="{badge_balance_class}">{badge_balance_value}</span>
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
        st.subheader("📈 Évolution financière")

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
        st.subheader("📄 Transactions")

        if data:
            df = pd.DataFrame(data).tail(4)

            rows = ""
            for _, row in df.iterrows():
                color = "#22c55e" if row["type"] == "income" else "#ef4444"
                sign = "+" if row["type"] == "income" else "-"

                rows += f"""
                <tr>
                    <td>{row['date']}</td>
                    <td>{row['type']}</td>
                    <td style="color:{color}; font-weight:600;">
                        {sign} {row['amount']} FCFA
                    </td>
                </tr>
                """

            st.markdown(f"""
            <table>
                <tr>
                    <th>Date</th>
                    <th>Type</th>
                    <th>Montant</th>
                </tr>
                {rows}
            </table>
            """, unsafe_allow_html=True)
        else:
            st.info("Aucune transaction")

        st.markdown('</div>', unsafe_allow_html=True)