import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
from babel.numbers import format_currency

def create_daily_rents_df(df):
    daily_rents_df = df.resample(rule='D', on='dteday').agg({
        "instant": "nunique",
        "season": "sum"
    })
    daily_rents_df = daily_rents_df.reset_index()
    daily_rents_df.rename(columns={
        "instant": "instant_count",
        "season": "revenue"
    }, inplace=True)
    
    return daily_rents_df

def create_bymonth_df(df):
    bymonth_df = df.groupby(by="mnth").instant.nunique().reset_index()
    bymonth_df.rename(columns={
        "instant": "instant_count"
    }, inplace=True)
    
    return bymonth_df

def create_byseason_df(df):
    byseason_df = df.groupby("season").instant.sum().sort_values(ascending=False).reset_index()

    map_dict = {1:'Spring', 2:'Summer', 3:'Autumn', 4:'Winter'}
    byseason_df['season_group'] = byseason_df['season'].map(map_dict)

    return byseason_df

mdata_df = pd.read_csv("main_data.csv")

datetime_columns = ["dteday", "date"]
mdata_df.sort_values(by="dteday", inplace=True)
mdata_df.reset_index(inplace=True)

datetime_columns = ["dteday"]

for column in datetime_columns:
    mdata_df[column] = pd.to_datetime(mdata_df[column])

min_date = mdata_df["dteday"].min()
max_date = mdata_df["dteday"].max()

with st.sidebar:
    st.image("https://img.freepik.com/free-vector/man-riding-bike_24908-81774.jpg?t=st=1714929795~exp=1714933395~hmac=4d893d6c31fcf770fff26a90ff19687d58a5152c83f0c5427986e1009cce721d&w=740")
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = mdata_df[(mdata_df["dteday"] >= str(start_date)) & 
                (mdata_df["dteday"] <= str(end_date))]

daily_rents_df = create_daily_rents_df(main_df)
bymonth_df = create_bymonth_df(main_df)
byseason_df = create_byseason_df(main_df)

st.header('Bike Sharing')

st.subheader('Nadia Monika Putri M132D4KX2285')

st.write(
    """
    ### Table of Hour
    """
)

st.write(mdata_df.head(500))

col1, col2 = st.columns(2)
with col1:
    total_rents = daily_rents_df.instant_count.sum()
    st.metric("Total Rents by Hour", value=total_rents)

with col2:
    total_revenue = format_currency(daily_rents_df.revenue.sum(), "AUD", locale='es_CO') 
    st.metric("Total Revenue", value=total_revenue)

fig, ax = plt.subplots(figsize=(20, 8))
ax.plot(
    daily_rents_df["dteday"],
    daily_rents_df["instant_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

plot_data = main_df['hr']

fig, ax = plt.subplots()
ax.hist(plot_data, bins=50, color="#90CAF9")
ax.set_xlabel('Hour')
ax.set_ylabel('instant')
ax.set_title('By Hour')

st.pyplot(fig)

st.subheader("By Month and Season")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(30, 15))
 
    colors = ["#D3D3D3", "#72BCD4", "#D3D3D3", "#D3D3D3", "#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#D3D3D3", "#D3D3D3"]

    sns.barplot(
        y="instant_count", 
        x="mnth",
        data=bymonth_df.sort_values(by="instant_count", ascending=False),
        palette=colors,
        ax=ax
    )
    # ax.set_title("by Month", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(30, 15))
    
    colors = ["#90CAF9", "#D3D3D3", "#90CAF9", "#D3D3D3"]
 
    sns.barplot(
        y="instant", 
        x="season_group",
        data=byseason_df.sort_values(by="season_group", ascending=False),
        palette=colors,
        ax=ax
    )
    # ax.set_title("by Season", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

vega_data = mdata_df.head(9000)[["instant", "mnth", "season"]]

st.vega_lite_chart(
   vega_data,
   {
       "mark": {"type": "circle", "tooltip": True},
       "encoding": {
           "x": {"field": "mnth", "type": "quantitative", "scale": {"domain": [1, 12]}},
           "y": {"field": "instant", "type": "quantitative"},
           "size": {"field": "season", "type": "quantitative"},
           "color": {"field": "season", "type": "quantitative"},
       },
   },
   width=800,
   height=400
)

st.subheader("By Holiday, Weekday, and Workingday")

chart_data = mdata_df.head(500)[["holiday", "weekday", "workingday"]]

st.line_chart(chart_data)

st.subheader("By Year, Season, and Month")
schart_data = mdata_df.head(9000)[["yr", "season", "mnth"]]
st.scatter_chart(schart_data)


st.caption('Copyright Nadia 2024')