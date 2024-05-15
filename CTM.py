import streamlit as st
import pandas as pd

st.set_page_config(page_title="CTM report", layout="wide")

uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        data = pd.read_excel(uploaded_file, sheet_name = 'By Item', header = 5)

        st.dataframe(data)
    
    except Exception as e:
      st.error(f"An error occurred: {e}")
      
