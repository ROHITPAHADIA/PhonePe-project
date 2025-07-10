import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import os

from plots.charts import (
    top_states_transaction_chart,
    quarterly_trend_chart,
    device_usage_chart,
    insurance_top_states_chart,
    insurance_trend_chart,
    user_growth_chart,
    user_conversion_gap_chart,
    statewise_comparison_chart,
)
from utils import fetch_dataframe

st.set_page_config(page_title="📊 PhonePe Insights Dashboard", layout="wide")
st.title("📊 PhonePe Data Insights Dashboard")

st.markdown("#### A unified view of PhonePe's usage, user behavior, insurance growth, and device engagement trends across India.")

# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Transactions", 
    "📱 Devices", 
    "📦 Insurance", 
    "👥 Users", 
    "🧠 Statewise KPIs"
])

# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.header("📊 Transactions Overview")

    query = """
    SELECT state, SUM(amount) AS total_amount
    FROM aggregated_transaction
    WHERE year = 2023 AND quarter = 4
    GROUP BY state
    ORDER BY total_amount DESC
    LIMIT 10;
    """
    df = fetch_dataframe(query)
    st.plotly_chart(top_states_transaction_chart(df), use_container_width=True)

    query2 = """
    SELECT state, year, quarter, SUM(amount) as total_amount
    FROM aggregated_transaction
    GROUP BY state, year, quarter
    HAVING state IN (
        SELECT state
        FROM aggregated_transaction
        WHERE year = 2023 AND quarter = 4
        GROUP BY state
        ORDER BY SUM(amount) DESC
        LIMIT 5
    );
    """
    df2 = fetch_dataframe(query2)
    st.plotly_chart(quarterly_trend_chart(df2), use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.header("📱 Device Usage and Engagement")

    # Year and Quarter Selectors
    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.selectbox("Select Year", fetch_dataframe("SELECT DISTINCT year FROM aggregated_user ORDER BY year DESC")['year'])
    with col2:
        selected_quarter = st.selectbox("Select Quarter", fetch_dataframe("SELECT DISTINCT quarter FROM aggregated_user ORDER BY quarter ASC")['quarter'])

    query = f"""
    SELECT brand, SUM(count) AS users, AVG(percentage) * 100 AS market_share
    FROM aggregated_user
    WHERE year = {selected_year} AND quarter = {selected_quarter}
    GROUP BY brand
    HAVING users > 0
    ORDER BY users DESC
    LIMIT 10;
    """
    df = fetch_dataframe(query)
    if not df.empty:
        st.plotly_chart(device_usage_chart(df), use_container_width=True)
    else:
        st.warning(f"No device engagement data found for Q{selected_quarter} {selected_year}.")

# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.header("📦 Insurance Penetration Overview")

    query = """
    SELECT state, SUM(amount) AS total_amount
    FROM aggregated_insurance
    WHERE year = 2023 AND quarter = 4
    GROUP BY state
    ORDER BY total_amount DESC
    LIMIT 10;
    """
    df = fetch_dataframe(query)
    if not df.empty:
        st.plotly_chart(insurance_top_states_chart(df), use_container_width=True)
    else:
        st.warning("No insurance data available for Q4 2023.")

    query2 = """
    SELECT state, year, quarter, SUM(amount) as total_amount
    FROM aggregated_insurance
    GROUP BY state, year, quarter
    HAVING state IN (
        SELECT state
        FROM aggregated_insurance
        GROUP BY state
        ORDER BY SUM(amount) DESC
        LIMIT 5
    );
    """
    df2 = fetch_dataframe(query2)
    if not df2.empty:
        st.plotly_chart(insurance_trend_chart(df2), use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    st.header("👥 User Growth & App Opens")

    query = """
    SELECT district, state, SUM(app_opens) as opens
    FROM map_user
    WHERE year = 2022 AND quarter = 4
    GROUP BY district, state
    ORDER BY opens DESC
    LIMIT 10;
    """
    df = fetch_dataframe(query)
    if not df.empty:
        st.plotly_chart(user_growth_chart(df), use_container_width=True)

    query2 = """
    SELECT district, state, SUM(registered_users) AS users, SUM(app_opens) AS opens
    FROM map_user
    GROUP BY district, state
    HAVING users > 10000 AND opens/users < 0.3
    ORDER BY opens/users ASC
    LIMIT 10;
    """
    df2 = fetch_dataframe(query2)
    if not df2.empty:
        st.plotly_chart(user_conversion_gap_chart(df2), use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
with tab5:
    st.header("🧠 Statewise Smart KPIs")

    # State Selector
    state_list = fetch_dataframe("SELECT DISTINCT state FROM aggregated_transaction ORDER BY state ASC")['state']
    selected_state = st.selectbox("Select a state", state_list)

    if selected_state:
        # ───────────────────────────────
        # 📌 Key Metrics for Selected State
        query = f"""
        SELECT
            '{selected_state}' AS state,
            (SELECT SUM(amount) FROM aggregated_transaction WHERE state = '{selected_state}') AS total_txn,
            (SELECT SUM(count) FROM aggregated_user WHERE state = '{selected_state}') AS total_users,
            (SELECT SUM(percentage * count) / SUM(count) * 100 FROM aggregated_user WHERE state = '{selected_state}') AS avg_open_rate,
            (SELECT SUM(amount) FROM aggregated_insurance WHERE state = '{selected_state}') AS total_insurance;
        """
        df = fetch_dataframe(query)

        if not df.empty:
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            kpi1.metric("Total Transactions", f"₹{df['total_txn'][0]:,.0f}")
            kpi2.metric("Total Users", f"{df['total_users'][0]:,}")
            kpi3.metric("Avg. Open Rate (%)", f"{df['avg_open_rate'][0]:.2f}")
            kpi4.metric("Total Insurance", f"₹{df['total_insurance'][0]:,.0f}")

            # ───────────────────────────────
            # 📈 KPI Trends Over Time
            trend_query = f"""
            SELECT
                at.year,
                at.quarter,
                SUM(at.amount) AS txn,
                (SELECT SUM(ai.amount) FROM aggregated_insurance ai WHERE ai.state = '{selected_state}' AND ai.year = at.year AND ai.quarter = at.quarter) AS insurance,
                (SELECT SUM(au.count) FROM aggregated_user au WHERE au.state = '{selected_state}' AND au.year = at.year AND au.quarter = at.quarter) AS users
            FROM aggregated_transaction at
            WHERE at.state = '{selected_state}'
            GROUP BY at.year, at.quarter
            ORDER BY at.year, at.quarter;
            """
            trend_df = fetch_dataframe(trend_query)

            if not trend_df.empty:
                trend_df["year_quarter"] = trend_df["year"].astype(str) + " Q" + trend_df["quarter"].astype(str)
                st.subheader("📈 KPI Trends Over Time")
                st.line_chart(trend_df.set_index("year_quarter")[["txn", "insurance", "users"]])

            # ───────────────────────────────
            # 📊 State vs National Average
            national_query = """
            SELECT
                (SELECT SUM(amount) FROM aggregated_transaction) AS total_txn,
                (SELECT SUM(count) FROM aggregated_user) AS total_users,
                (SELECT SUM(percentage * count) / SUM(count) * 100 FROM aggregated_user) AS avg_open_rate,
                (SELECT SUM(amount) FROM aggregated_insurance) AS total_insurance;
            """
            national_df = fetch_dataframe(national_query)

            if not national_df.empty:
                comp_df = pd.DataFrame({
                    "KPI": ["Total Transactions", "Total Users", "Avg. Open Rate (%)", "Total Insurance"],
                    "Selected State": [
                        df['total_txn'][0],
                        df['total_users'][0],
                        df['avg_open_rate'][0],
                        df['total_insurance'][0],
                    ],
                    "National Average": [
                        national_df['total_txn'][0],
                        national_df['total_users'][0],
                        national_df['avg_open_rate'][0],
                        national_df['total_insurance'][0],
                    ]
                })

                comp_df["% of National Avg"] = (comp_df["Selected State"] / comp_df["National Average"]) * 100

                st.subheader("📊 State vs National Average")
                st.dataframe(
                    comp_df.style.format({
                        "Selected State": "₹{:,.0f}",
                        "National Average": "₹{:,.0f}",
                        "% of National Avg": "{:.1f}%"
                    }).set_properties(**{"text-align": "left"})
                )
        else:
            st.info("No metrics available for the selected state.")
