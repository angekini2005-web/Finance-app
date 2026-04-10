import json
import os
import pandas as pd

TRANSACTIONS_FILE = "data/transactions.json"
EXPORT_FILE = "data/reports/transactions_report.xlsx"

def export_transactions_to_excel():
    if not os.path.exists(TRANSACTIONS_FILE):
        print("❌ Aucun fichier de transactions")
        return

    with open(TRANSACTIONS_FILE, "r") as f:
        transactions = json.load(f)

    if not transactions:
        print("❌ Aucune transaction à exporter")
        return

    df = pd.DataFrame(transactions)

    os.makedirs("data/reports", exist_ok=True)

    df.to_excel(EXPORT_FILE, index=False)

    print(f"✅ Export réussi : {EXPORT_FILE}")

    if not os.path.exists("data/reports"):
        if os.path.exists("data/reports") and not os.path.isdir("data/reports"):
         print("❌ 'reports' existe mais ce n'est pas un dossier")
         return

    os.makedirs("data/reports", exist_ok=True)