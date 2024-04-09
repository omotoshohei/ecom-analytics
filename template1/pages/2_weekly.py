import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import MaxNLocator


df_merge = pd.read_csv("data/temp1/output/merge.csv")
df_daily_sales = pd.read_csv("data/temp1/output/daily_sales.csv")
df_daily_sales_detail = pd.read_csv("data/temp1/output/daily_sales_detail.csv")

df_merge['birth_date'] = pd.to_datetime(df_merge['birth_date'], format='%Y-%m-%d')
df_merge['transaction_date'] = pd.to_datetime(df_merge['transaction_date'], format='%Y-%m-%d')
df_merge['shipping_date'] = pd.to_datetime(df_merge['shipping_date'], format='%Y-%m-%d')
df_merge['cancellation_date'] = pd.to_datetime(df_merge['cancellation_date'], format='%Y-%m-%d')
df_daily_sales['transaction_date'] = pd.to_datetime(df_daily_sales['transaction_date'], format='%Y-%m-%d')
df_daily_sales_detail['transaction_date'] = pd.to_datetime(df_daily_sales_detail['transaction_date'], format='%Y-%m-%d')

st.set_page_config(layout="wide")

st.title("Weekly Sales Report")
st.write("The data is available from 2019.04.01 to 2020.10.01")


### ----------------------------------------------------------------------------------------------------
### ----------------------------------------------------------------------------------------------------
st.header("1. Line Chart")

df_weekly_sales = df_daily_sales.copy()
df_weekly_sales['transaction_date'] = pd.to_datetime(df_weekly_sales['transaction_date'])
df_weekly_sales = df_weekly_sales.set_index('transaction_date').resample("W").sum().reset_index()
df_weekly_sales['week'] = df_weekly_sales['transaction_date'].dt.strftime('%Y-%U')

fig, ax = plt.subplots(figsize=(15,10))
ax.plot(df_weekly_sales['week'], df_weekly_sales['sales'], linestyle='-', color='green', label='Weekly Sales')

y_formatter = ScalarFormatter(useOffset=False)
y_formatter.set_scientific(False)
ax.yaxis.set_major_formatter(y_formatter)

ax.set_title('Weekly Sales')
ax.set_xlabel('Week')  # Set the x-axis label rotation to 90 degrees
ax.set_ylabel('Sales')
ax.set_xticklabels(df_weekly_sales['week'], rotation=90)
ax.legend()
ax.grid(True)
st.pyplot(fig)

### ----------------------------------------------------------------------------------------------------
### ----------------------------------------------------------------------------------------------------
st.header("2. Bar Chart - Year Comparison")

df_weekly_sales_2019 = df_daily_sales_detail[df_daily_sales_detail['year'] == 2019].groupby("week").agg({"sales":"sum"}).reset_index()
df_weekly_sales_2019.rename(columns={"sales": "2019_sales"}, inplace=True)
df_weekly_sales_2020 = df_daily_sales_detail[df_daily_sales_detail['year'] == 2020].groupby("week").agg({"sales":"sum"}).reset_index()
df_weekly_sales_2020.rename(columns={"sales": "2020_sales"}, inplace=True)
df_weekly_sales_by_year = pd.merge(df_weekly_sales_2019, df_weekly_sales_2020, on="week", how="outer").set_index("week").sort_values('week')
df_weekly_sales_by_year['YoY'] = df_weekly_sales_by_year.apply(
    lambda row: int(round((row['2020_sales'] / row['2019_sales'] - 1) * 100))
    if pd.notnull(row['2019_sales']) and pd.notnull(row['2020_sales']) else "-", axis=1
)
df_weekly_sales_by_year['YoY'] = df_weekly_sales_by_year['YoY'].apply(
    lambda x: f"{x}%" if isinstance(x, int) else x)
df_weekly_sales_by_year['2019_sales'] = df_weekly_sales_by_year['2019_sales'].fillna(0).astype(int)
df_weekly_sales_by_year['2020_sales'] = df_weekly_sales_by_year['2020_sales'].fillna(0).astype(int)
df_weekly_sales_by_year['WoW_2019'] = df_weekly_sales_by_year['2019_sales'].pct_change().fillna(0)
df_weekly_sales_by_year['WoW_2020'] = df_weekly_sales_by_year['2020_sales'].pct_change().fillna(0)
df_weekly_sales_by_year['WoW_2019'] = df_weekly_sales_by_year['WoW_2019'].apply(lambda x: f"{x:.0%}")
df_weekly_sales_by_year['WoW_2020'] = df_weekly_sales_by_year['WoW_2020'].apply(lambda x: f"{x:.0%}")
df_weekly_sales_by_year['WoW_2019'] = df_weekly_sales_by_year['WoW_2019'].apply(lambda x: "0%" if x == "inf%" else x)
df_weekly_sales_by_year['WoW_2020'] = df_weekly_sales_by_year['WoW_2020'].apply(lambda x: "0%" if x == "inf%" else x)

fig, ax = plt.subplots(figsize=(15,10))
bar_width = 0.35

index = np.arange(df_weekly_sales_by_year.shape[0])
bar1 = ax.bar(index, df_weekly_sales_by_year['2019_sales'], bar_width, color='lightgreen', label='2019 Sales')
bar2 = ax.bar(index + bar_width, df_weekly_sales_by_year['2020_sales'], bar_width, color='green', label='2020 Sales')

# fix y-axis to show the exact number
y_formatter = ScalarFormatter(useOffset=False)
y_formatter.set_scientific(False)
ax.yaxis.set_major_formatter(y_formatter)

ax.set_xlabel('Week')
ax.set_ylabel('Sales')
ax.set_title('weekly Sales for 2019 vs 2020')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(df_weekly_sales_by_year.index)
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Table View - Year Comparison
df_weekly_sales_by_year_table = df_weekly_sales_by_year.copy()
df_weekly_sales_by_year_table = df_weekly_sales_by_year_table.reset_index()
st.dataframe(df_weekly_sales_by_year_table, height=1890, width=500,hide_index=True)

### ----------------------------------------------------------------------------------------------------
### ----------------------------------------------------------------------------------------------------
st.header("3. Weekly Sales by Category")
df_merge['transaction_week'] = df_merge['transaction_date'].dt.strftime('%Y-%U')
df_weekly_sales_by_category = pd.pivot_table(df_merge, index='transaction_week', columns='category', values=['sales'],aggfunc='sum')

fig, ax = plt.subplots()
ax.plot(df_weekly_sales_by_category.index, df_weekly_sales_by_category['sales', 'タブレット'], label='タブレット')
ax.plot(df_weekly_sales_by_category.index, df_weekly_sales_by_category['sales', 'デスクトップ'], label='デスクトップ')
ax.plot(df_weekly_sales_by_category.index, df_weekly_sales_by_category['sales', 'ノートPC'], label='ノートPC')
ax.plot(df_weekly_sales_by_category.index, df_weekly_sales_by_category['sales', '周辺機器'], label='周辺機器')

# Fix the y-axis to show the exact number
y_formatter = ScalarFormatter(useOffset=False)
y_formatter.set_scientific(False)
ax.yaxis.set_major_formatter(y_formatter)

# Rotate x-axis labels and set their font size
ax.tick_params(axis='x', labelsize=7, rotation=45)

# Set the y-axis label font size
ax.tick_params(axis='y', labelsize=7)

# Ensure only a certain number of labels are shown
ax.xaxis.set_major_locator(MaxNLocator(integer=True, prune='both', nbins=10))

# Show legend
ax.legend()
# Display the plot in Streamlit
st.pyplot(fig)