import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Set tema visualisasi
sns.set(style='dark')

# ======================= FUNGSI HELPER =======================

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_date').agg({
        "order_id": "nunique",
        "total_price": "sum"
    }).reset_index()
    daily_orders_df.rename(columns={"order_id": "order_count", "total_price": "revenue"}, inplace=True)
    return daily_orders_df

def create_sum_order_items_df(df):
    return df.groupby("product_name").quantity_x.sum().sort_values(ascending=False).reset_index()

def create_bygender_df(df):
    bygender_df = df.groupby("gender").customer_id.nunique().reset_index()
    bygender_df.rename(columns={"customer_id": "customer_count"}, inplace=True)
    return bygender_df

def create_byage_df(df):
    byage_df = df.groupby("age_group").customer_id.nunique().reset_index()
    byage_df.rename(columns={"customer_id": "customer_count"}, inplace=True)
    byage_df['age_group'] = pd.Categorical(byage_df['age_group'], ["Youth", "Adults", "Seniors"])
    return byage_df

def create_bystate_df(df):
    bystate_df = df.groupby("state").customer_id.nunique().reset_index()
    bystate_df.rename(columns={"customer_id": "customer_count"}, inplace=True)
    return bystate_df

def create_rfm_df(df):
    rfm_df = df.groupby("customer_id", as_index=False).agg({
        "order_date": "max",
        "order_id": "nunique",
        "total_price": "sum"
    })
    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = df["order_date"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    return rfm_df

# ======================= DATA LOADING & FILTER =======================

all_df = pd.read_csv("all_data.csv")

datetime_columns = ["order_date", "delivery_date"]
for col in datetime_columns:
    all_df[col] = pd.to_datetime(all_df[col])
all_df.sort_values(by="order_date", inplace=True)
all_df.reset_index(drop=True, inplace=True)

min_date = all_df["order_date"].min()
max_date = all_df["order_date"].max()

# ======================= SIDEBAR =======================
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_date"] >= pd.to_datetime(start_date)) &
                 (all_df["order_date"] <= pd.to_datetime(end_date))]

# ======================= PROSES DATAFRAME =======================
daily_orders_df = create_daily_orders_df(main_df)
sum_order_items_df = create_sum_order_items_df(main_df)
bygender_df = create_bygender_df(main_df)
byage_df = create_byage_df(main_df)
bystate_df = create_bystate_df(main_df)
rfm_df = create_rfm_df(main_df)

# ======================= DASHBOARD =======================

st.header('Dicoding Collection Dashboard :sparkles:')
st.subheader('Daily Orders')

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Orders", value=daily_orders_df.order_count.sum())
with col2:
    revenue = format_currency(daily_orders_df.revenue.sum(), "AUD", locale='es_CO')
    st.metric("Total Revenue", value=revenue)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(daily_orders_df["order_date"], daily_orders_df["order_count"], marker='o', linewidth=2, color="#90CAF9")
ax.set_xlabel("Date")
ax.set_ylabel("Order Count")
ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=10)
st.pyplot(fig)

# ======================= PRODUK TERBAIK & TERBURUK =======================
st.subheader("Best & Worst Performing Product")
fig, ax = plt.subplots(1, 2, figsize=(24, 10))
colors = ["#90CAF9"] + ["#D3D3D3"] * 4

# Best
sns.barplot(x="quantity_x", y="product_name", data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
ax[0].set_title("Best Performing Product", fontsize=18)

# Worst
sns.barplot(x="quantity_x", y="product_name", data=sum_order_items_df.sort_values(by="quantity_x").head(5), palette=colors, ax=ax[1])
ax[1].set_title("Worst Performing Product", fontsize=18)

st.pyplot(fig)

# ======================= DEMOGRAFI PELANGGAN =======================
st.subheader("Customer Demographics")
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x="gender", y="customer_count", data=bygender_df, palette="pastel", ax=ax)
    ax.set_title("Customer by Gender")
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x="age_group", y="customer_count", data=byage_df, palette="Set2", ax=ax)
    ax.set_title("Customer by Age Group")
    st.pyplot(fig)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(y="state", x="customer_count", data=bystate_df.sort_values(by="customer_count", ascending=False), palette="Blues_r", ax=ax)
ax.set_title("Customer by State")
st.pyplot(fig)

# ======================= ANALISIS RFM =======================
st.subheader("Best Customer Based on RFM Parameters")

col1, col2, col3 = st.columns(3)
col1.metric("Average Recency (days)", round(rfm_df.recency.mean(), 1))
col2.metric("Average Frequency", round(rfm_df.frequency.mean(), 2))
col3.metric("Average Monetary", format_currency(rfm_df.monetary.mean(), "AUD", locale='es_CO'))

fig, ax = plt.subplots(1, 3, figsize=(24, 6))

# Recency
sns.barplot(x="customer_id", y="recency", data=rfm_df.sort_values(by="recency").head(5), ax=ax[0], palette="coolwarm")
ax[0].set_title("Top 5 Customers by Recency")

# Frequency
sns.barplot(x="customer_id", y="frequency", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), ax=ax[1], palette="coolwarm")
ax[1].set_title("Top 5 Customers by Frequency")

# Monetary
sns.barplot(x="customer_id", y="monetary", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), ax=ax[2], palette="coolwarm")
ax[2].set_title("Top 5 Customers by Monetary")

st.pyplot(fig)
