import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib
from matplotlib.ticker import ScalarFormatter

df_daily_sales = pd.read_csv("../data/temp1/output/daily_sales.csv")
df_daily_sales_detail = pd.read_csv("../data/temp1/output/daily_sales_detail.csv")

df_daily_sales['transaction_date'] = pd.to_datetime(df_daily_sales['transaction_date'], format='%Y-%m-%d')
df_daily_sales_detail['transaction_date'] = pd.to_datetime(df_daily_sales_detail['transaction_date'], format='%Y-%m-%d')

st.set_page_config(layout="wide")




# Initialize the session state for 'authenticated' key
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Display the introduction on the home page
st.title('Weekly Sales Report')



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
        if password == "777":
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
    st.header("Monthly Sales Report")

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

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
# else:
#     # If not authenticated, show a warning
#     st.warning('Please enter your password and click login to continue.')
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------







