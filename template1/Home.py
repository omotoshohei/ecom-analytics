import streamlit as st

# Set the page title and favicon
st.set_page_config(page_title="Ecommerce Analytics - Home", page_icon=":bar_chart:")

# Initialize the session state for 'authenticated' key
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Display the introduction on the home page
st.title('Ecommerce Analytics Template')

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
    # Main page content goes here
    st.markdown("""
    Ecommerce Analytics Template provides you with an intuitive interface to explore your sales data through interactive charts, tables, and graphs. Dive into your sales performance, uncover trends, and make data-driven decisions with ease.
    
    ### Features:
    - **Dashboard Overview**: Get a quick snapshot of your sales KPIs at a glance.
    - **Trend Analysis**: Understand your sales trends over time to forecast future performance.
    - **Product Breakdown**: Analyze sales by product categories, regions, or any custom dimension.
    - **Performance Tracking**: Track your sales team's performance and manage targets.
    
    ### How to Navigate:
    - Use the sidebar to switch between different analytics pages.
    - Select specific filters to view customized data sets.
    - Hover over charts and graphs for more detailed information.
    
    Get started by selecting an option from the sidebar menu and let Sales Insights reveal the story behind your data.
    """)
else:
    # If not authenticated, show a warning
    st.warning('Please enter your password and click login to continue.')