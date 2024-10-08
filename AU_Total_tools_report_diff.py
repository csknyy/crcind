import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(page_title="AU Total Tools report difference", layout="wide")

uploaded_file_0 = st.file_uploader("Upload the prior month's file")
uploaded_file_1 = st.file_uploader("Upload the current month's file")

if uploaded_file_0 is not None and uploaded_file_1 is not None:
    try:
        prior_month = pd.read_excel(uploaded_file_0, engine = 'openpyxl', header = 1)
        current_month = pd.read_excel(uploaded_file_1, engine = 'openpyxl', header = 1)
        
        st.dataframe(prior_month)
        st.dataframe(current_month)

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a CSV file to get started.")
