from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import json
import os

TRANSACTIONS_FILE = "data/transactions.json"
PROJECTS_FILE = "data/projects.json"

def export_pdf():
    if not os.path.exists("data/reports"):
        os.makedirs("data/reports")

    doc = SimpleDocTemplate("data/reports/rapport_financier.pdf")
    styles = getSampleStyleSheet()

    elements = []

    # Charger transactions
    if os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, "r") as f:
            transactions = json.load(f)
    else:
        transactions = []

    income = 0
    expense = 0

    for t in transactions:
        if t["type"] == "income":
            income += t["amount"]
        else:
            expense += t["amount"]

    profit = income - expense

    elements.append(Paragraph("RAPPORT FINANCIER", styles["Title"]))
    elements.append(Paragraph(f"Revenus : {income}", styles["Normal"]))
    elements.append(Paragraph(f"Dépenses : {expense}", styles["Normal"]))
    elements.append(Paragraph(f"Profit : {profit}", styles["Normal"]))

    doc.build(elements)

    print("✅ PDF généré : data/reports/rapport_financier.pdf")