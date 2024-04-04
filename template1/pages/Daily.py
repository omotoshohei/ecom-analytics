import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib
from matplotlib.ticker import ScalarFormatter

password_key = st.secrets['PASSWORD']

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

# Initialize the session state for 'authenticated' key
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Display the introduction on the home page
st.title('Daily Sales Report')
st.write("The data is available from 2019.04.01 to 2020.10.01")


#-------------------------------------------------------------------------
#--------------------------- Log in Auth Start ---------------------------
#-------------------------------------------------------------------------
# Only show the login form if the user is not authenticated
if not st.session_state['authenticated']:
    # Placeholder for the password field and login button
    password_placeholder = st.empty()
    login_button_placeholder = st.empty()

    password = password_placeholder.text_input("Enter your password", type="password")

    # Check the entered password
    if login_button_placeholder.button('Login'):
        if password == password_key:
            st.session_state['authenticated'] = True
            password_placeholder.empty()  # Clear the password input
            login_button_placeholder.empty()  # Remove the login button
            # If you want to clear the success message after showing it, use another placeholder
        else:
            st.error('Wrong password')

# If authenticated, show the main page content
if st.session_state['authenticated']:
#-------------------------------------------------------------------------
#--------------------------- Log in Auth End -----------------------------
#-------------------------------------------------------------------------

    # Main page content goes here

    ### Daily Sales Report ------------------------------------------------------------------------------------
    ### -------------------------------------------------------------------------------------------------------
    st.header("1. All Period")
    st.subheader("1-1. Line Chart")
    # Line Chart - All Period
    ### ---------------------

    df_daily_sales_line_chart = df_daily_sales.copy()
    df_daily_sales_line_chart.set_index('transaction_date', inplace=True)

    fig, ax = plt.subplots(figsize=(15,8))
    ax.plot(df_daily_sales_line_chart['sales'], linestyle='-', color='green', label='sales')

    y_formatter = ScalarFormatter(useOffset=False)
    y_formatter.set_scientific(False)
    ax.yaxis.set_major_formatter(y_formatter)

    ax.set_title('Daily Sales')
    ax.set_xlabel('Dates')
    ax.set_ylabel('Sales')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)



    # Moving Average
    st.subheader("1-2. Moving Average - 30 days")

    df_daily_sales_moving_avg = df_daily_sales.copy()
    df_daily_sales_moving_avg['moving_avg'] = df_daily_sales_moving_avg['sales'].rolling(window=30).mean()


    df_daily_sales_moving_avg.set_index('transaction_date', inplace=True)

    fig, ax = plt.subplots(figsize=(15,10))
    ax.plot(df_daily_sales_moving_avg.index, df_daily_sales_moving_avg['moving_avg'], linestyle='--', color='orange', label='30 days moving avg')

    y_formatter = ScalarFormatter(useOffset=False)
    y_formatter.set_scientific(False)
    ax.yaxis.set_major_formatter(y_formatter)

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

    ### Select the Data Range ------------------------------------------------------------------------------------
    ### -------------------------------------------------------------------------------------------------------
    st.header("2. Select Date Range for Daily Sales")

    # Streamlit date input for user to pick start and end date

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input('Start date', value=pd.to_datetime('2020-01-01'))
    with col2:
        end_date = st.date_input('End date', value=pd.to_datetime('2020-03-30'))


    st.subheader("2-1. Line Chart")

    # Filter by Date
    df_daily_sales_select_dates = df_daily_sales[["transaction_date", "sales"]]
    df_daily_sales_select_dates.set_index('transaction_date', inplace=True)
    df_daily_sales_select_dates = df_daily_sales_select_dates.loc[start_date:end_date]

    # Plot
    fig, ax = plt.subplots(figsize=(15,10))
    ax.plot(df_daily_sales_select_dates.index, df_daily_sales_select_dates['sales'], linestyle='-', color='green', label='Sales')

    y_formatter = ScalarFormatter(useOffset=False)
    y_formatter.set_scientific(False)
    ax.yaxis.set_major_formatter(y_formatter)

    ax.set_title('Daily Sales')
    ax.set_xlabel('Dates')
    ax.set_ylabel('Sales')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    # Moving Average
    st.subheader("2-2. Daily Sales - 30 Days Moving Average ")


    df_daily_sales_moving_avg = df_daily_sales.copy()
    df_daily_sales_moving_avg['moving_avg'] = df_daily_sales_moving_avg['sales'].rolling(window=30).mean()

    df_daily_sales_moving_avg.set_index('transaction_date', inplace=True)
    df_daily_sales_moving_avg = df_daily_sales_moving_avg.loc[start_date:end_date]

    fig, ax = plt.subplots(figsize=(15,10))
    ax.plot(df_daily_sales_moving_avg.index, df_daily_sales_moving_avg['moving_avg'], linestyle='--', color='orange', label='30 days moving avg')

    y_formatter = ScalarFormatter(useOffset=False)
    y_formatter.set_scientific(False)
    ax.yaxis.set_major_formatter(y_formatter)

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


#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
# else:
#     # If not authenticated, show a warning
#     st.warning('Please enter your password and click login to continue.')
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
