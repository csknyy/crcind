import streamlit as st
import pandas as pd

st.set_page_config(page_title="CTM report", layout="wide")

uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        data = pd.read_excel(uploaded_file, sheet_name = 'By Item', header = 5)
        data = data.iloc[:-1]
        data.columns.values[4] = 'Item Description'

        data_grouped1 = data.groupby(by='Item Description').sum()[['Sales $','GP $']]
        
        total_sales = data_grouped1['Sales $'].sum()
        data_grouped1['CTS %'] = data_grouped1['Sales $'] / total_sales
        
        data_grouped1['GP %'] = data_grouped1['GP $'] / data_grouped1['Sales $']

        data_grouped1['CTM'] = data_grouped1['CTS'] * data_grouped1['GP %']

        total_CTM = data_grouped1['CTM'].sum()

        data_grouped1['CTM %'] = 100 * data_grouped1['CTM'] / total_CTM
        
        st.dataframe(data_grouped1.style.format(subset=["Sales $"], formatter="${:,.2f}").format(subset=["CTS %"], formatter="%{:,.2f}").format(subset=["GP $"], formatter="${:,.2f}").format(subset=["GP %"], formatter="%{:,.2f}").format(subset=["CTM %"], formatter="%{:,.2f}"))
        st.dataframe(data)
    
    except Exception as e:
      st.error(f"An error occurred: {e}")
      
