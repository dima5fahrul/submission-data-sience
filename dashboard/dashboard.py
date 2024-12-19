import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
import os.path
sns.set(style="dark")

def create_daily_pm25_df(df, station):
    daily_pm25_df = df[df.station == station].resample(rule="D", on="date").agg({
        "PM2.5": "mean"
    })
    daily_pm25_df = daily_pm25_df.reset_index()
    daily_pm25_df.rename(columns={
        "PM2.5": "pm25_mean"
    }, inplace=True)

    return daily_pm25_df
  
def create_daily_pm10_df(df, station):
    daily_pm10_df = df[df.station == station].resample(rule="D", on="date").agg({
        "PM10": "mean"
    })
    daily_pm10_df = daily_pm10_df.reset_index()
    daily_pm10_df.rename(columns={
        "PM10": "pm10_mean"
    }, inplace=True)

    return daily_pm10_df
  
def create_daily_so2_df(df, station):
    daily_so2_df = df[df.station == station].resample(rule="D", on="date").agg({
        "SO2": "mean"
    })
    daily_so2_df = daily_so2_df.reset_index()
    daily_so2_df.rename(columns={
        "SO2": "so2_mean"
    }, inplace=True)

    return daily_so2_df
  
def create_daily_co_df(df, station):
    daily_co_df = df[df.station == station].resample(rule="D", on="date").agg({
        "CO": "mean"
    })
    daily_co_df = daily_co_df.reset_index()
    daily_co_df.rename(columns={
        "CO": "co_mean"
    }, inplace=True)

    return daily_co_df
  
def create_daily_o3_df(df, station):
    daily_o3_df = df[df.station == station].resample(rule="D", on="date").agg({
        "O3": "mean"
    })
    daily_o3_df = daily_o3_df.reset_index()
    daily_o3_df.rename(columns={
        "O3": "o3_mean"
    }, inplace=True)

    return daily_o3_df
  
def create_daily_no2_df(df, station):
    daily_no2_df = df[df.station == station].resample(rule="D", on="date").agg({
        "NO2": "mean"
    })
    daily_no2_df = daily_no2_df.reset_index()
    daily_no2_df.rename(columns={
        "NO2": "no2_mean"
    }, inplace=True)

    return daily_no2_df
  
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  
def average_pm25_per_day_of_week(daily_mean_df):
  daily_mean_df['day_of_week'] = daily_mean_df['date'].dt.day_name()
  daily_mean_df['day_of_week'] = pd.Categorical(daily_mean_df['day_of_week'], days_order, ordered=True)
  
  daily_mean_df = daily_mean_df.groupby('day_of_week').agg({
      'pm25_mean': 'mean'
  }).reindex(days_order)
  
  return daily_mean_df

def average_pm10_per_day_of_week(daily_mean_df):
  daily_mean_df['day_of_week'] = daily_mean_df['date'].dt.day_name()
  daily_mean_df['day_of_week'] = pd.Categorical(daily_mean_df['day_of_week'], days_order, ordered=True)
  
  daily_mean_df = daily_mean_df.groupby('day_of_week').agg({
      'pm10_mean': 'mean'
  }).reindex(days_order)
  
  return daily_mean_df

def worst_air_quality(df):
    worst_air_quality = df.groupby("station").agg({
        "PM2.5": "mean",
        "PM10": "mean",
        "SO2": "mean",
        "CO": "mean",
        "O3": "mean",
        "NO2": "mean"
    }).sort_values(by=["PM2.5", "PM10", "SO2", "CO", "O3", "NO2"], ascending=False)
    
    return worst_air_quality
  
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "submission-data-sience/dashboard/all_cities_air_quality.csv")

@st.cache_data
def load_data():
    return pd.read_csv(DATA)
  
df = load_data()
df['date'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])

min_date = df.date.min().date()
max_date = df.date.max().date()

with st.sidebar:
    st.title("Air Quality Dashboard")
    st.write("This dashboard is created to visualize air quality data from various cities.")
    st.write("Select a city to view the air quality data.")
    city = st.selectbox("City", df.station.unique())
    
    start_date, end_date = st.date_input(
        label="Date Range", min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
main_df = df[(df["date"] >= str(start_date)) & (df["date"] <= str(end_date))]
    
pm25_df = create_daily_pm25_df(main_df, city)
pm10_df = create_daily_pm10_df(main_df, city)
so2_df = create_daily_so2_df(main_df, city)
co_df = create_daily_co_df(main_df, city)
o3_df = create_daily_o3_df(main_df, city)
no2_df = create_daily_no2_df(main_df, city)

st.header(city)

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(
  pm25_df["date"],
  pm25_df["pm25_mean"],
  marker='o',
  linewidth=2,
  color='skyblue'
)

ax.axhline(y=75, color='red', linestyle='--', linewidth=1.5, label='24h Threshold by Chinese AQI Standard')
ax.axhline(y=15, color='blue', linestyle='--', linewidth=1.5, label='24h Threshold by WHO Standard')

plt.xticks(rotation=45)
plt.title("PM2.5 (µg/m³) Daily Average", fontsize=25)
plt.xlabel("Date", fontsize=15)
plt.ylabel("PM2.5 (µg/m³)", fontsize=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)

ax.legend()

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(
  pm10_df["date"],
  pm10_df["pm10_mean"],
  marker='o',
  linewidth=2,
  color='skyblue'
)

ax.axhline(y=150, color='red', linestyle='--', linewidth=1.5, label='24h Threshold by Chinese AQI Standard')
ax.axhline(y=45, color='blue', linestyle='--', linewidth=1.5, label='24h Threshold by WHO Standard')

plt.xticks(rotation=45)
plt.title("PM10 (µg/m³) Daily Average", fontsize=25)
plt.xlabel("Date", fontsize=15)
plt.ylabel("PM10 (µg/m³)", fontsize=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)

ax.legend()

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(
  so2_df["date"],
  so2_df["so2_mean"],
  marker='o',
  linewidth=2,
  color='skyblue'
)

ax.axhline(y=150, color='red', linestyle='--', linewidth=1.5, label='24h Threshold by Chinese AQI Standard')
ax.axhline(y=40, color='blue', linestyle='--', linewidth=1.5, label='24h Threshold by WHO Standard')

plt.xticks(rotation=45)
plt.title("SO2 (µg/m³) Daily Average", fontsize=25)
plt.xlabel("Date", fontsize=15)
plt.ylabel("SO2 (µg/m³)", fontsize=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)

ax.legend()

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(
  co_df["date"],
  co_df["co_mean"],
  marker='o',
  linewidth=2,
  color='skyblue'
)

ax.axhline(y=10, color='red', linestyle='--', linewidth=1.5, label='24h Threshold by Chinese AQI Standard')
ax.axhline(y=9, color='blue', linestyle='--', linewidth=1.5, label='24h Threshold by WHO Standard')

plt.xticks(rotation=45)
plt.title("CO (mg/m³) Daily Average", fontsize=25)
plt.xlabel("Date", fontsize=15)
plt.ylabel("CO (mg/m³)", fontsize=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)

ax.legend()

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(
  o3_df["date"],
  o3_df["o3_mean"],
  marker='o',
  linewidth=2,
  color='skyblue'
)

ax.axhline(y=160, color='red', linestyle='--', linewidth=1.5, label='1h Threshold by Chinese AQI Standard')
ax.axhline(y=180, color='blue', linestyle='--', linewidth=1.5, label='1h Threshold by WHO Standard')

plt.xticks(rotation=45)
plt.title("O3 (µg/m³) Daily Average", fontsize=25)
plt.xlabel("Date", fontsize=15)
plt.ylabel("O3 (µg/m³)", fontsize=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)

ax.legend()

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(
  no2_df["date"],
  no2_df["no2_mean"],
  marker='o',
  linewidth=2,
  color='skyblue'
)

ax.axhline(y=80, color='red', linestyle='--', linewidth=1.5, label='24h Threshold by Chinese AQI Standard')
ax.axhline(y=40, color='blue', linestyle='--', linewidth=1.5, label='24h Threshold by WHO Standard')

plt.xticks(rotation=45)
plt.title("NO2 (µg/m³) Daily Average", fontsize=25)
plt.xlabel("Date", fontsize=15)
plt.ylabel("NO2 (µg/m³)", fontsize=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)

ax.legend()

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

fig, ax = plt.subplots(figsize=(12, 6))
pm25_day_of_week = average_pm25_per_day_of_week(pm25_df)
ax.bar(pm25_day_of_week.index, pm25_day_of_week['pm25_mean'], color='lightcoral')

plt.title("PM2.5 (µg/m³) Average per Day of Week", fontsize=25)
plt.xlabel("Day of Week", fontsize=15)
plt.ylabel("PM2.5 (µg/m³)", fontsize=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

fig, ax = plt.subplots(figsize=(12, 6))
pm10_day_of_week = average_pm10_per_day_of_week(pm10_df)
ax.bar(pm10_day_of_week.index, pm10_day_of_week['pm10_mean'], color='lightgreen')

plt.title("PM10 (µg/m³) Average per Day of Week", fontsize=25)
plt.xlabel("Day of Week", fontsize=15)
plt.ylabel("PM10 (µg/m³)", fontsize=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

worst_air_quality_df = worst_air_quality(df)
st.subheader("Worst Air Quality")
fig, ax = plt.subplots(figsize=(20, 10))
bar_width = 0.2
x = np.arange(6)

offset_changping = x - 1.5 * bar_width
offset_dingling = x - 0.5 * bar_width
offset_dongsi = x + 0.5 * bar_width
offset_gucheng = x + 1.5 * bar_width

ax.bar(
  offset_changping,
  worst_air_quality_df.loc["Changping", ["PM2.5", "PM10", "SO2", "CO", "O3", "NO2"]],
  width=bar_width,
  label="Changping",
  color='skyblue'
)

ax.bar(
  offset_dingling,
  worst_air_quality_df.loc["Dingling", ["PM2.5", "PM10", "SO2", "CO", "O3", "NO2"]],
  width=bar_width,
  label="Dingling",
  color='lightcoral'
)

ax.bar(
  offset_dongsi,
  worst_air_quality_df.loc["Dongsi", ["PM2.5", "PM10", "SO2", "CO", "O3", "NO2"]],
  width=bar_width,
  label="Dongsi",
  color='lightgreen'
)

ax.bar(
  offset_gucheng,
  worst_air_quality_df.loc["Gucheng", ["PM2.5", "PM10", "SO2", "CO", "O3", "NO2"]],
  width=bar_width,
  label="Gucheng",
  color='orange'
)

plt.title("Worst Air Quality", fontsize=25)
plt.xlabel("Pollutant", fontsize=15)
plt.ylabel("Value", fontsize=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)

ax.set_xticks(x)
ax.set_xticklabels(["PM2.5", "PM10", "SO2", "CO", "O3", "NO2"])
ax.legend()

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)