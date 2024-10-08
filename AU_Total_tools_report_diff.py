import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(page_title="AU Total Tools report difference", layout="wide")

uploaded_file_0 = st.file_uploader("Upload the prior month's file")
uploaded_file_1 = st.file_uploader("Upload the current month's file")

if uploaded_file_0 is not None and uploaded_file_1 is not None:
    #try:
    prior_month = pd.read_excel(uploaded_file_0, engine = 'openpyxl', header = 1)
    prior_month = prior_month.rename(columns={prior_month.columns[0]: 'Store'})
    prior_month.iloc[0,0] = 'Summary'
    prior_month_sliced = prior_month.iloc[:, :3]
    
    current_month = pd.read_excel(uploaded_file_1, engine = 'openpyxl', header = 1)
    current_month = current_month.rename(columns={current_month.columns[0]: 'Store'})
    current_month.iloc[0,0] = 'Summary'
    
    merged_data = pd.merge(current_month, prior_month_sliced, on='Store', how='left')
    st.dataframe(merged_data)
    
    merged_data.iloc[:, -2] = pd.to_numeric(merged_data.iloc[:, -2], errors='coerce').fillna(0)
    merged_data.iloc[:, -1] = pd.to_numeric(merged_data.iloc[:, -1], errors='coerce').fillna(0)
    merged_data.iloc[:, 1] = pd.to_numeric(merged_data.iloc[:, 1], errors='coerce').fillna(0)
    
    merged_data['Monthly Sales'] = merged_data.iloc[:, 1] - merged_data.iloc[:, -2]
    merged_data['Monthly Sales'] = merged_data['Monthly Sales'].replace(0, np.nan)
    
    merged_data['Monthly Profit'] = merged_data.iloc[:, 2] - merged_data.iloc[:, -2]
    merged_data['Monthly Profit'] = merged_data['Monthly Profit'].replace(0, np.nan)
    
    merged_data['Monthly GP%'] = np.where(merged_data['Monthly Sales'] != 0, merged_data['Monthly Profit'] / merged_data['Monthly Sales'], 0)
    
    st.dataframe(merged_data)

    #except Exception as e:
        #st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a CSV file to get started.")
