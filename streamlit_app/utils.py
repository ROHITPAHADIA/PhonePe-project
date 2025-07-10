import sqlite3
import pandas as pd
import os
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "phonepe_data.db")

@st.cache_data(show_spinner=False)
def fetch_dataframe(query, params=None):
    # Always create a fresh connection for thread safety
    with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
        df = pd.read_sql_query(query, conn, params=params)
    return df
