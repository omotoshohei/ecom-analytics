import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import MaxNLocator


import pandas as pd
import streamlit as st

# Assuming df_merge is read in correctly from your CSV and dates are parsed as datetime objects.
df_merge = pd.read_csv("data/temp1/output/merge.csv", parse_dates=['birth_date', 'transaction_date', 'shipping_date', 'cancellation_date'])
df_daily_sales = pd.read_csv("data/temp1/output/daily_sales.csv", parse_dates=['transaction_date'])
df_daily_sales_detail = pd.read_csv("data/temp1/output/daily_sales_detail.csv", parse_dates=['transaction_date'])

st.set_page_config(layout="wide")

st.title("Product Report")
st.write("The data is available from 2019.04.01 to 2020.10.01")
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input('Start date', value=pd.to_datetime('2020-01-01'))
with col2:
    end_date = st.date_input('End date', value=pd.to_datetime('2020-03-30'))

# Convert the dates to datetime64[ns] to match the DataFrame's dtype
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)
# Filter the dataframe by the selected date range
df_filtered = df_merge[(df_merge['transaction_date'] >= start_date) & (df_merge['transaction_date'] <= end_date)]

# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------
st.header("1. Product Category Performance")

# Sum the sales for each category within the filtered date range
df_product_category = df_filtered.groupby('category', as_index=False)['sales'].sum()

fig, ax = plt.subplots(figsize=(10, 8))
ax.bar(df_product_category['category'], df_product_category['sales'])
# Fix the y-axis to show the exact number
y_formatter = ScalarFormatter(useOffset=False)
y_formatter.set_scientific(False)
ax.yaxis.set_major_formatter(y_formatter)
st.pyplot(fig)

# Display the DataFrame in Streamlit
st.table(df_product_category)


# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------
st.header("2. Product Performance")

# Sum the sales for each category within the filtered date range
df_product = df_filtered.groupby('product_name', as_index=False)['sales'].sum().sort_values('sales', ascending=False)

fig, ax = plt.subplots(figsize=(10, 8))
ax.bar(df_product['product_name'], df_product['sales'])

# Fix the y-axis to show the exact number
y_formatter = ScalarFormatter(useOffset=False)
y_formatter.set_scientific(False)
ax.yaxis.set_major_formatter(y_formatter)
# Rotate x-axis labels and set their font size
ax.tick_params(axis='x', labelsize=5, rotation=90)
ax.tick_params(axis='y', labelsize=7)

st.pyplot(fig)
# Display the DataFrame in Streamlit
st.table(df_product)