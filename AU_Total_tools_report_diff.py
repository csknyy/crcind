import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(page_title="AU Total Tools report difference", layout="wide")

uploaded_file_0 = st.file_uploader("Upload the prior month's file")
uploaded_file_1 = st.file_uploader("Upload the current month's file")

if uploaded_file_0 is not None and uploaded_file_1 is not None:
    try:
        prior_month = pd.read_excel(uploaded_file_0, engine = 'openpyxl', header = 1)
        prior_month_sliced = prior_month.iloc[:, :4]
        current_month = pd.read_excel(uploaded_file_1, engine = 'openpyxl', header = 1)
        merged_data = pd.merge(current_month, prior_month, on='Item ID', how='left')

        st.dataframe(prior_month)
        st.dataframe(current_month)
        st.dataframe(merged_data)

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a CSV file to get started.")
