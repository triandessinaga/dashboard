import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


# Load dataset
# Load dataset
# df = pd.read_csv("PRSA_Data_Aotizhongxin_20130301-20170228.csv")  # Gantilah dengan nama file kamu
df = pd.read_csv("PRSA_Data_Aotizhongxin_20130301-20170228.csv")  # Gantilah dengan nama file kamu
df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])

# Set Seaborn style
sns.set(style='whitegrid')

# Sidebar
st.sidebar.title("Air Quality Dashboard")
st.sidebar.markdown("## Filter by Date Range")

min_date = df['datetime'].min()
max_date = df['datetime'].max()

start_date, end_date = st.sidebar.date_input(
    label="Select date range",
    min_value=min_date.date(),
    max_value=max_date.date(),
    value=[min_date.date(), max_date.date()]
)

# Filter by date
mask = (df['datetime'].dt.date >= start_date) & (df['datetime'].dt.date <= end_date)
filtered_df = df[mask]

# Header
st.title(" Air Quality Monitoring Dashboard")
st.markdown("Tracking air pollution metrics from multiple stations.")

# Metrics
st.subheader(" Key Air Quality Metrics")
st.metric("Average PM2.5", round(filtered_df["PM2.5"].mean(), 2))
st.metric("Average NO2", round(filtered_df["NO2"].mean(), 2))
st.metric("Average CO", round(filtered_df["CO"].mean(), 2))

# Time Series Plot
st.subheader(" PM2.5 Trend Over Time")
fig, ax = plt.subplots(figsize=(15, 5))
sns.lineplot(data=filtered_df, x="datetime", y="PM2.5", hue="station", ax=ax, palette="flare")
ax.set_title("Hourly PM2.5 Levels")
ax.set_ylabel("PM2.5")
ax.set_xlabel("Time")
st.pyplot(fig)

# Barplot per Station
st.subheader(" Average PM2.5 per Station")
avg_pm25 = filtered_df.groupby("station")["PM2.5"].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=avg_pm25, x="station", y="PM2.5", palette="magma", ax=ax)
ax.set_title("Average PM2.5 by Station")
ax.set_ylabel("PM2.5")
ax.set_xlabel("Station")
st.pyplot(fig)

# CO vs NO2 Correlation
st.subheader(" CO vs NO2 Relationship")
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(data=filtered_df, x="CO", y="NO2", hue="station", style="station", palette="rocket", ax=ax)
ax.set_title("CO vs NO2 Concentrations")
ax.set_xlabel("CO")
ax.set_ylabel("NO2")
st.pyplot(fig)

# Wind Speed Distribution
st.subheader("chr(0x1F33F) Wind Speed Distribution")

st.subheader(f"{chr(0x1F33F)} Wind Speed Distribution")
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(data=filtered_df, x="station", y="WSPM", palette="coolwarm", ax=ax)
ax.set_title("Wind Speed (WSPM) per Station")
st.pyplot(fig)
