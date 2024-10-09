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
    prior_month.set_index('Store', inplace=True)
    #prior_month.iloc[0,0] = 'Summary'
    prior_month_sliced = prior_month.iloc[:, :2]

    st.dataframe(prior_month_sliced)

    try:
        prior_month_sliced = prior_month_sliced.drop(index='Summary')
    except:
        pass
    
    current_month = pd.read_excel(uploaded_file_1, engine = 'openpyxl', header = 1)
    current_month = current_month.rename(columns={current_month.columns[0]: 'Store'})
    #current_month.iloc[0,0] = 'Summary'
    current_month.set_index('Store', inplace=True)

    try:
        current_month = current_month.drop(index='Summary')
    except:
        pass
    
    merged_data = pd.merge(current_month, prior_month_sliced, left_index=True, right_index=True, how='left')
    st.dataframe(merged_data)

    merged_data = merged_data.apply(pd.to_numeric, errors='coerce').fillna(0)
    #merged_data.iloc[:, 0] = pd.to_numeric(merged_data.iloc[:, 0], errors='coerce').fillna(0)
    #merged_data.iloc[:, 1] = pd.to_numeric(merged_data.iloc[:, 1], errors='coerce').fillna(0)
    #merged_data.iloc[:, 5] = pd.to_numeric(merged_data.iloc[:, 5], errors='coerce').fillna(0)
    #merged_data.iloc[:, -2] = pd.to_numeric(merged_data.iloc[:, -2], errors='coerce').fillna(0)
    #merged_data.iloc[:, -1] = pd.to_numeric(merged_data.iloc[:, -1], errors='coerce').fillna(0)
    
    
    merged_data['Monthly Sales'] = merged_data.iloc[:, 0] - merged_data.iloc[:, -2]
    merged_data['Monthly Sales'] = merged_data['Monthly Sales'].replace(0, np.nan)
    
    merged_data['Monthly Profit'] = merged_data.iloc[:, 1] - merged_data.iloc[:, -2]
    merged_data['Monthly Profit'] = merged_data['Monthly Profit'].replace(0, np.nan)
    
    merged_data['Monthly GP%'] = np.where(merged_data['Monthly Sales'] != 0, merged_data['Monthly Profit'] / merged_data['Monthly Sales'], 0)

    merged_data.loc['Summary', :] = 0
    for col in merged_data.columns:
        merged_data.loc['Summary', col] = merged_data[col].sum()

    merged_data.iloc[-1, 2] = merged_data.iloc[:, 1].sum() / merged_data.iloc[:, 0].sum()
    
    merged_data['delete'] = np.where((merged_data.iloc[:, 3] != 0) | (merged_data.iloc[:, 5] != 0), merged_data.iloc[:, 3] / merged_data.iloc[:, 5], 0)


    merged_data = merged_data.apply(pd.to_numeric, errors='coerce').fillna(0)
    
    temp_total = merged_data.iloc[:-1, -1].sum()
    st.text(temp_total )
    st.text(merged_data.iloc[:-1, 3].sum())
    
    merged_data.iloc[-1, 5] = merged_data.iloc[:-1, 3].sum() / merged_data.iloc[:-1, -1].sum()
    
    


    
    
    st.dataframe(merged_data)

    #except Exception as e:
        #st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a CSV file to get started.")
