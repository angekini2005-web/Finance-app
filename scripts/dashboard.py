import streamlit as st
import matplotlib.pyplot as plt
from scripts.accounts import load_transactions

def get_financial_data():

    username = st.session_state.user
    transactions = load_transactions(username)

    income = 0
    expense = 0

    for t in transactions:
        if t["type"] == "income":
            income += t["amount"]
        else:
            expense += t["amount"]

    balance = income - expense

    return income, expense, balance


def show_kpis():

    income, expense, balance = get_financial_data()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("💰 Revenus", f"{income} FCFA")

    with col2:
        st.metric("💸 Dépenses", f"{expense} FCFA")

    with col3:
        st.metric("📈 Solde", f"{balance} FCFA")


def show_bar_chart():

    income, expense, _ = get_financial_data()

    labels = ["Revenus", "Dépenses"]
    values = [income, expense]

    fig, ax = plt.subplots()
    ax.bar(labels, values)

    st.subheader("📊 Revenus vs Dépenses")
    st.pyplot(fig)


def show_pie_chart():

    income, expense, _ = get_financial_data()

    labels = ["Revenus", "Dépenses"]
    sizes = [income, expense]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%")

    st.subheader("🥧 Répartition")
    st.pyplot(fig)


def show_dashboard():

    st.title("📊 Dashboard Financier")

    show_kpis()
    st.write("---")

    show_bar_chart()
    show_pie_chart()