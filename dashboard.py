import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

# API URL
api_url = "http://127.0.0.1:8000/VoltageA-N"  # Replace with your API

# Function to fetch data from the API
def fetch_data():
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()  # Assuming the API returns JSON
    else:
        return {"error": "Failed to fetch data"}

# Streamlit app
st.title("Scheinder Vavg Voltage")

# Refresh the app every 5 seconds
st_autorefresh(interval=500, key="data_refresh")

# Display data from the API
data = fetch_data()

# Increase font size using HTML
st.markdown(f"<h2 style='font-size: 30px;'>Voltage: {data[0]} V</h2>", unsafe_allow_html=True)
