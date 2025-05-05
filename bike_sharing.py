import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Load dataset
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Parse dates
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Sidebar date filter
st.sidebar.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

start_date, end_date = st.sidebar.date_input(
    label='Select Date Range',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

filtered_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & 
                     (day_df['dteday'] <= pd.to_datetime(end_date))]

# Header
st.header('Bike Sharing Dashboard 🚴‍♂️')
st.subheader('Daily Rentals Overview')

# Daily Count Plot
st.metric("Total Rentals", value=int(filtered_df['cnt'].sum()))
st.metric("Average Rentals / Day", value=round(filtered_df['cnt'].mean(), 2))

fig, ax = plt.subplots(figsize=(16, 6))
sns.lineplot(data=filtered_df, x='dteday', y='cnt', marker='o', ax=ax, color="#90CAF9")
ax.set_title('Daily Rental Trends', fontsize=20)
ax.set_xlabel('Date')
ax.set_ylabel('Count')
st.pyplot(fig)

# Rentals by Season
st.subheader("Rentals by Season")

season_map = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}
filtered_df['season'] = filtered_df['season'].map(season_map)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=filtered_df, x='season', y='cnt', palette='Blues_d', ax=ax)
ax.set_title("Total Rentals by Season")
st.pyplot(fig)

# Rentals by Working Day
st.subheader("Rentals: Working Day vs Holiday")

labels = ['Holiday', 'Working Day']
workingday_counts = filtered_df.groupby('workingday')['cnt'].sum().reset_index()
workingday_counts['Label'] = workingday_counts['workingday'].map({0: "Holiday", 1: "Working Day"})

fig, ax = plt.subplots(figsize=(6, 6))
sns.barplot(data=workingday_counts, x='Label', y='cnt', palette='pastel', ax=ax)
ax.set_ylabel("Total Rentals")
ax.set_xlabel(None)
st.pyplot(fig)

# Hourly Trend for Selected Date
st.subheader("Hourly Rental Trend (Example Date)")

example_date = filtered_df['dteday'].dt.date.iloc[0]
hourly_day = hour_df[hour_df['dteday'] == str(example_date)]

fig, ax = plt.subplots(figsize=(14, 6))
sns.lineplot(data=hourly_day, x='hr', y='cnt', marker='o', ax=ax, color="#FFA07A")
ax.set_title(f'Hourly Rentals on {example_date}')
ax.set_xlabel('Hour of Day')
ax.set_ylabel('Count')
st.pyplot(fig)

# Weather impact
st.subheader("Rentals by Weather Situation")

weather_map = {
    1: "Clear",
    2: "Mist + Cloudy",
    3: "Light Snow / Rain",
    4: "Heavy Rain"
}
filtered_df['weather_sit'] = filtered_df['weathersit'].map(weather_map)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=filtered_df, x='weather_sit', y='cnt', palette='coolwarm', ax=ax)
ax.set_title("Rentals by Weather Condition")
st.pyplot(fig)
