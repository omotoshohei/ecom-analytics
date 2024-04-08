import streamlit as st

# Set the page title and favicon
st.set_page_config(page_title="Ecom Sales Report Template", page_icon=":bar_chart:")
password_key = st.secrets['PASSWORD']




# Display the introduction on the home page
st.title('Ecom Sales Report Template')

st.markdown("""

The "Ecom Sales Report Template" is designed for Ecommerce businesses, enabling the monitoring of sales trends on a daily, weekly, and monthly basis.

### Features

- Track both daily and long-term sales trends for Ecommerce operations.
- Reports are developed using Python, with tools like Pandas, Matplotlib, and Streamlit.

### Advantages over other Reports

- Offers greater flexibility in data processing and visualization compared to standard BI tools.
- Capable of displaying in a web browser with additional functionalities like password-protected access.
- Incorporates advanced features such as machine learning and AI.

### Future Development

- Integration of predictive analytics utilizing machine learning.
- Addition of commentary and recommendation features using the ChatGPT API.

### Developer

- [Shohei Omoto](https://www.linkedin.com/in/shoheiomoto/)
- A Growth Marketer and Data Scientist based in Tokyo.

### Please Note

- Access to the Insight page requires a password for security verification; currently, the page does not include content.
- Displayed sales and other data are based on sample datasets.
- For inquiries on using this template, please reach out to [Shohei Omoto](https://www.linkedin.com/in/shoheiomoto/).
- Please note that unauthorized reproduction or use is prohibited.
""")
