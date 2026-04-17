import streamlit as st
import json
import pandas as pd

def show_history():
    try:
        with open("data/transactions.json") as f:
            data = json.load(f)
    except:
        data = []

    if data:
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.info("Aucune transaction")