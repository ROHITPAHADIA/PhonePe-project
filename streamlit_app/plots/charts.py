import plotly.express as px
import pandas as pd

# ─────────────────────────────────────────────────────────────────────────────
def top_states_transaction_chart(df):
    fig = px.bar(
        df,
        x="total_amount",
        y="state",
        orientation="h",
        color="total_amount",
        color_continuous_scale="viridis",
        title="Top 10 States by Transaction Amount (Q4 2023)",
        labels={"total_amount": "Transaction Amount (INR)", "state": "State"},
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    return fig

def quarterly_trend_chart(df):
    df["year_quarter"] = df["year"].astype(str) + " Q" + df["quarter"].astype(str)
    fig = px.line(
        df,
        x="year_quarter",
        y="total_amount",
        color="state",
        markers=True,
        title="Quarterly Transaction Trend (Top 5 States)",
        labels={"year_quarter": "Year - Quarter", "total_amount": "Transaction Amount (INR)"},
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def device_usage_chart(df):
    fig = px.scatter(
        df,
        x="market_share",
        y="users",
        size="users",
        color="market_share",
        hover_name="brand",
        title="Device Brand Share vs Total Users",
        labels={"market_share": "Market Share (%)", "users": "Registered Users"},
        color_continuous_scale="viridis"
    )
    return fig


def insurance_top_states_chart(df):
    fig = px.bar(
        df,
        x="total_amount",
        y="state",
        orientation="h",
        color="total_amount",
        color_continuous_scale="plasma",
        title="Top 10 States by Insurance Amount (Q4 2023)",
        labels={"total_amount": "Insurance Amount (INR)", "state": "State"},
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    return fig

def insurance_trend_chart(df):
    df["year_quarter"] = df["year"].astype(str) + " Q" + df["quarter"].astype(str)
    fig = px.line(
        df,
        x="year_quarter",
        y="total_amount",
        color="state",
        markers=True,
        title="Insurance Transaction Trend (Top States)",
        labels={"year_quarter": "Year - Quarter", "total_amount": "Insurance Amount (INR)"},
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def user_growth_chart(df):
    fig = px.bar(
        df,
        x="opens",
        y="district",
        orientation="h",
        color="opens",
        color_continuous_scale="blues",
        title="Top Districts by App Opens (Q4 2022)",
        labels={"opens": "App Opens", "district": "District"},
        hover_data=["state"]
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    return fig

def user_conversion_gap_chart(df):
    df["open_rate"] = df["opens"] / df["users"]
    fig = px.bar(
        df,
        x="open_rate",
        y="district",
        orientation="h",
        color="open_rate",
        color_continuous_scale="reds",
        title="Low Engagement Districts: Low App Opens per User",
        labels={"open_rate": "Open Rate", "district": "District"},
        hover_data=["state", "users", "opens"]
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    return fig

def statewise_comparison_chart(long_df):
    fig = px.bar(
        long_df,
        x="Value",
        y="KPI",
        orientation="h",
        color="KPI",
        text="Value",
        title=f"📊 Key Metrics for {long_df.iloc[0]['state'].title()}",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    fig.update_layout(showlegend=False)
    return fig

