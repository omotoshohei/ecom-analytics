import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib

df_merge = pd.read_csv("../data/temp1/output/merge.csv")
df_daily_sales = pd.read_csv("../data/temp1/output/daily_sales.csv")
df_daily_sales_detail = pd.read_csv("../data/temp1/output/daily_sales_detail.csv")

df_merge['birth_date'] = pd.to_datetime(df_merge['birth_date'], format='%Y-%m-%d')
df_merge['transaction_date'] = pd.to_datetime(df_merge['transaction_date'], format='%Y-%m-%d')
df_merge['shipping_date'] = pd.to_datetime(df_merge['shipping_date'], format='%Y-%m-%d')
df_merge['cancellation_date'] = pd.to_datetime(df_merge['cancellation_date'], format='%Y-%m-%d')
df_daily_sales['transaction_date'] = pd.to_datetime(df_daily_sales['transaction_date'], format='%Y-%m-%d')
df_daily_sales_detail['transaction_date'] = pd.to_datetime(df_daily_sales_detail['transaction_date'], format='%Y-%m-%d')



st.title("Ecommerce Analytics Template")
st.write("This template is to display the data for Ecommerce website.")

### Daily Sales Report -------------------------
st.header("1. Daily Sales Report")

# Line Chart
st.subheader("1-1. Line Graph - All Period")
fig, ax = plt.subplots(figsize=(15,10))
ax.plot(df_daily_sales['sales'], linestyle='-', color='green', label='sales')

ax.set_title('Daily Sales')
ax.set_xlabel('Dates')
ax.set_ylabel('Sales')
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Table
st.subheader("1-2. Table View - All Period")
st.dataframe(df_daily_sales)

# Moving Average
st.subheader("1-3. Moving Average - 30 days")

df_daily_sales_moving_avg = df_daily_sales.copy()
df_daily_sales_moving_avg['moving_avg'] = df_daily_sales_moving_avg['sales'].rolling(window=30).mean()

start_date = "2020-01-01"
end_date = "2020-03-30"
df_daily_sales_moving_avg.set_index('transaction_date', inplace=True)
df_daily_sales_moving_avg = df_daily_sales_moving_avg.loc[start_date:end_date]

fig, ax = plt.subplots(figsize=(15,10))
ax.plot(df_daily_sales_moving_avg.index, df_daily_sales_moving_avg['moving_avg'], linestyle='--', color='orange', label='30 days moving avg')

ax.set_title('Daily Sales - 30 Days Moving Average')
ax.set_xlabel('Dates')
ax.set_ylabel('Sales - Moving Average')
ax.legend()
ax.grid(True)
st.pyplot(fig)
text_moving_average= """
Moving average is a statistical method used to analyze a set of data points by creating a series of averages of different subsets of the full data set. 
It is widely used in time series analysis to smooth out short-term fluctuations and highlight longer-term trends or cycles. 
The 'moving' part is due to the window of data points used in the calculation as it moves across the data set.
"""
st.write(text_moving_average)

### Monthly Sales Report -------------------------
st.header("2. Monthly Sales Report")

# Line Chart
st.subheader("2-1. Line Chart")

df_monthly_sales = df_daily_sales.copy()
df_monthly_sales.set_index('transaction_date', inplace=True)
df_monthly_sales = df_monthly_sales.resample("MS").sum()
df_monthly_sales = df_monthly_sales[["sales"]]
df_monthly_sales = df_monthly_sales.rename_axis('month')
df_monthly_sales.index = df_monthly_sales.index.strftime('%Y-%m')

fig, ax = plt.subplots(figsize=(15,10))
ax.bar(df_monthly_sales.index, df_monthly_sales['sales'], color='green', label='Monthly Sales')

ax.set_title('Monthly Sales')
ax.set_xlabel('Month')
ax.set_ylabel('Sales')
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Line Chart - Year Comparison
st.subheader("2-1. Line Chart - Year Comparison")

df_monthly_sales_2019 = df_daily_sales_detail[df_daily_sales_detail['year'] == 2019].groupby("month").agg({"sales":"sum"}).reset_index()
df_monthly_sales_2019.rename(columns={"sales": "2019_sales"}, inplace=True)
df_monthly_sales_2020 = df_daily_sales_detail[df_daily_sales_detail['year'] == 2020].groupby("month").agg({"sales":"sum"}).reset_index()
df_monthly_sales_2020.rename(columns={"sales": "2020_sales"}, inplace=True)
df_monthly_sales_by_year = pd.merge(df_monthly_sales_2019, df_monthly_sales_2020, on="month", how="outer").set_index("month").sort_values('month')
df_monthly_sales_by_year['YoY'] = df_monthly_sales_by_year.apply(
    lambda row: int(round((row['2020_sales'] / row['2019_sales'] - 1) * 100))
    if pd.notnull(row['2019_sales']) and pd.notnull(row['2020_sales']) else "-", axis=1
)
df_monthly_sales_by_year['YoY'] = df_monthly_sales_by_year['YoY'].apply(
    lambda x: f"{x}%" if isinstance(x, int) else x)
df_monthly_sales_by_year['2019_sales'] = df_monthly_sales_by_year['2019_sales'].fillna(0).astype(int)
df_monthly_sales_by_year['2020_sales'] = df_monthly_sales_by_year['2020_sales'].fillna(0).astype(int)
df_monthly_sales_by_year['MoM_2019'] = df_monthly_sales_by_year['2019_sales'].pct_change().fillna(0)
df_monthly_sales_by_year['MoM_2020'] = df_monthly_sales_by_year['2020_sales'].pct_change().fillna(0)
df_monthly_sales_by_year['MoM_2019'] = df_monthly_sales_by_year['MoM_2019'].apply(lambda x: f"{x:.0%}")
df_monthly_sales_by_year['MoM_2020'] = df_monthly_sales_by_year['MoM_2020'].apply(lambda x: f"{x:.0%}")
df_monthly_sales_by_year['MoM_2019'] = df_monthly_sales_by_year['MoM_2019'].apply(lambda x: "0%" if x == "inf%" else x)
df_monthly_sales_by_year['MoM_2020'] = df_monthly_sales_by_year['MoM_2020'].apply(lambda x: "0%" if x == "inf%" else x)

fig, ax = plt.subplots(figsize=(15,10))
bar_width = 0.35

index = np.arange(df_monthly_sales_by_year.shape[0])
bar1 = ax.bar(index, df_monthly_sales_by_year['2019_sales'], bar_width, color='lightgreen', label='2019 Sales')
bar2 = ax.bar(index + bar_width, df_monthly_sales_by_year['2020_sales'], bar_width, color='green', label='2020 Sales')

from matplotlib.ticker import ScalarFormatter
y_formatter = ScalarFormatter(useOffset=False)
y_formatter.set_scientific(False)
ax.yaxis.set_major_formatter(y_formatter)

ax.set_xlabel('Month')
ax.set_ylabel('Sales')
ax.set_title('Monthly Sales for 2019 vs 2020')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(df_monthly_sales_by_year.index)
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Table View - Year Comparison
st.subheader("2-3. Table View - Year Comparison")

df_monthly_sales_by_year.index.name = 'Month'

df_monthly_sales_by_year_reset = df_monthly_sales_by_year.reset_index()
st.table(df_monthly_sales_by_year_reset)


