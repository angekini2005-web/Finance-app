import json
import os
from datetime import datetime

def get_user_file(username):
    return f"data/transactions_{username}.json"


def load_transactions(username):
    file = get_user_file(username)

    if not os.path.exists(file):
        return []

    with open(file, "r") as f:
        return json.load(f)


def save_transactions(username, transactions):
    file = get_user_file(username)

    with open(file, "w") as f:
        json.dump(transactions, f, indent=4)


def add_transaction(username, amount, type_, project=None):

    transactions = load_transactions(username)

    transactions.append({
        "amount": amount,
        "type": type_,
        "project": project,
        "date": str(datetime.now())
    })

    save_transactions(username, transactions)


def calculate_balances(username):

    transactions = load_transactions(username)

    balance = 0

    for t in transactions:
        if t["type"] == "income":
            balance += t["amount"]
        else:
            balance -= t["amount"]

    return balance