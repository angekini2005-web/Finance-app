import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
from scripts.accounts import load_transactions

def forecast():

    st.title("📈 Prévisions financières")

    # 🔐 Vérifier utilisateur
    username = st.session_state.get("user", None)

    if not username:
        st.error("Utilisateur non connecté")
        return

    # 📥 Charger transactions
    transactions = load_transactions(username)

    if not transactions:
        st.warning("Pas assez de données")
        return

    try:
        # Trier par date
        transactions.sort(key=lambda x: x["date"])

        dates = []
        balance = 0
        balances = []

        for t in transactions:
            date = datetime.fromisoformat(t["date"])
            dates.append(date)

            if t["type"] == "income":
                balance += t["amount"]
            else:
                balance -= t["amount"]

            balances.append(balance)

        # 📊 Prévision
        future_dates = []
        future_balances = []

        trend = 0
        if len(balances) >= 2:
            trend = balances[-1] - balances[-2]

        last_date = dates[-1]
        last_balance = balances[-1]

        for i in range(30):
            next_date = last_date + timedelta(days=i+1)
            last_balance += trend

            future_dates.append(next_date)
            future_balances.append(last_balance)

        # 📈 Graphique
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=dates,
            y=balances,
            mode='lines',
            name='Historique'
        ))

        fig.add_trace(go.Scatter(
            x=future_dates,
            y=future_balances,
            mode='lines',
            name='Prévision',
            line=dict(dash='dash')
        ))

        fig.update_layout(
            template="plotly_dark",
            hovermode="x unified",
            title="Évolution du solde"
        )

        st.plotly_chart(fig, use_container_width=True)

        # 🧠 Analyse
        st.subheader("🧠 Analyse")

        if trend > 0:
            st.success("Tendance positive 📈")
        elif trend < 0:
            st.error("Tendance négative 📉")
        else:
            st.warning("Tendance stable")

    except Exception as e:
        st.error(f"Erreur dans les prévisions : {e}")