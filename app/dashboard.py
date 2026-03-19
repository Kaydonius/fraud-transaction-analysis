import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os


# Database connection
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "transactions.db")

# use cache data to deal w/ database queries
# connect to DB
@st.cache_data
def query(sql):
    with sqlite3.connect(DB_PATH) as connection:
        df = pd.read_sql_query(sql, connection)
    return df

# configure default settings of page
st.set_page_config(page_title="Fraud Analytics Dashboard", layout="wide")
st.title("Fraud Transaction Analytics")

# begin filtering
@st.cache_data
def load_full():
    return query("SELECT * FROM transaction_data")

df_full = load_full()

# sidebar filters
st.sidebar.header("Filters")

type_options = df_full["type"].unique().tolist()
selected_types = st.sidebar.multiselect("Transaction Type", type_options, default=type_options)

amount_min = float(df_full["amount"].min())
amount_max = float(df_full["amount"].max())
amount_range = st.sidebar.slider("Amount Range", amount_min, amount_max, (amount_min, amount_max))

step_min = int(df_full["step"].min())
step_max = int(df_full["step"].max())
step_range = st.sidebar.slider("Time Step Range", step_min, step_max, (step_min, step_max))

# applying filters
df = df_full[
    (df_full["type"].isin(selected_types)) &
    (df_full["amount"] >= amount_range[0]) &
    (df_full["amount"] <= amount_range[1]) &
    (df_full["step"] >= step_range[0]) &
    (df_full["step"] <= step_range[1])
]

# KPIS
st.header("Key Metrics")
total = len(df)
fraud_count = int(df["isfraud"].sum())
fraud_rate = round(fraud_count / total * 100, 4) if total > 0 else 0
avg_amount = round(df["amount"].mean(), 2) if total > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Transactions", f"{total:,}")
col2.metric("Fraud Count", f"{fraud_count:,}")
col3.metric("Fraud Rate", f"{fraud_rate}%")
col4.metric("Avg Transaction Amount", f"${avg_amount:,.2f}")

st.divider()

# Rows: Fraud trend and fraud by type
r1c1, r1c2 = st.columns(2)

with r1c1:
    st.subheader("Fraud Volume Over Time")
    trend = df.groupby("step")["isfraud"].sum().reset_index(name="fraud_count")
    fig_trend = px.line(trend, x="step", y="fraud_count",
                        labels={"step": "Time Step (hours)", "fraud_count": "Fraud Count"})
    st.plotly_chart(fig_trend, use_container_width=True)

with r1c2:
    st.subheader("Fraud Rate by Transaction Type")
    by_type = df.groupby("type").agg(
        total=("isfraud", "count"),
        fraud_count=("isfraud", "sum")
    ).reset_index()
    by_type["fraud_rate"] = round(by_type["fraud_count"] / by_type["total"] * 100, 4)
    fig_type = px.bar(by_type, x="type", y="fraud_rate", text="fraud_count",
                      labels={"type": "Transaction Type", "fraud_rate": "Fraud Rate (%)"},
                      color="fraud_rate", color_continuous_scale="Reds")
    st.plotly_chart(fig_type, use_container_width=True)

# Rows: Fraud by amount range and fraud by hour
r2c1, r2c2 = st.columns(2)

with r2c1:
    st.subheader("Fraud Rate by Amount Range")
    bins = [0, 1000, 10000, 100000, 1000000, float("inf")]
    labels = ["Under 1K", "1K-10K", "10K-100K", "100K-1M", "1M+"]
    df["amount_range"] = pd.cut(df["amount"], bins=bins, labels=labels, right=False)
    by_amount = df.groupby("amount_range", observed=True).agg(
        total=("isfraud", "count"),
        fraud_count=("isfraud", "sum")
    ).reset_index()
    by_amount["fraud_rate"] = round(by_amount["fraud_count"] / by_amount["total"] * 100, 4)
    fig_amount = px.bar(by_amount, x="amount_range", y="fraud_rate", text="fraud_count",
                        labels={"amount_range": "Amount Range", "fraud_rate": "Fraud Rate (%)"},
                        color="fraud_rate", color_continuous_scale="Reds")
    st.plotly_chart(fig_amount, use_container_width=True)

with r2c2:
    st.subheader("Fraud Rate by Hour of Day")
    if "hour_of_day" in df.columns:
        by_hour = df.groupby("hour_of_day").agg(
            total=("isfraud", "count"),
            fraud_count=("isfraud", "sum")
        ).reset_index()
        by_hour["fraud_rate"] = round(by_hour["fraud_count"] / by_hour["total"] * 100, 4)
        fig_hour = px.bar(by_hour, x="hour_of_day", y="fraud_rate",
                          labels={"hour_of_day": "Hour of Day", "fraud_rate": "Fraud Rate (%)"},
                          color="fraud_rate", color_continuous_scale="Reds")
        st.plotly_chart(fig_hour, use_container_width=True)
    else:
        st.info("Run features.py to generate `hour_of_day` column.")

# Rows: fraud vs non fraud amount distribution
st.subheader("Transaction Amount Distribution: Fraud vs Non-Fraud")
df["fraud_label"] = df["isfraud"].map({0: "Non-Fraud", 1: "Fraud"})
fig_hist = px.histogram(df, x="amount", color="fraud_label", nbins=100,
                        barmode="overlay", opacity=0.6, log_y=True,
                        labels={"amount": "Transaction Amount", "fraud_label": ""},
                        color_discrete_map={"Non-Fraud": "#636EFA", "Fraud": "#EF553B"})
st.plotly_chart(fig_hist, use_container_width=True)

st.divider()

# Rows: balance inconsistencies
st.subheader("Balance Inconsistencies (Origin)")
inconsistencies = df[abs(df["oldbalanceorg"] - df["amount"] - df["newbalanceorig"]) > 0.01].copy()
inconsistencies["expected_new_balance"] = inconsistencies["oldbalanceorg"] - inconsistencies["amount"]
inconsistencies["discrepancy"] = inconsistencies["newbalanceorig"] - inconsistencies["expected_new_balance"]
inconsistencies = (inconsistencies[["nameorig", "namedest", "oldbalanceorg", "newbalanceorig", 
                                     "amount", "expected_new_balance", "discrepancy"]]
                   .sort_values("discrepancy", key=abs, ascending=False)
                   .head(100))
st.dataframe(inconsistencies, use_container_width=True, hide_index=True)
