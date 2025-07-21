import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

st.set_page_config(page_title="Mitre 10 OOS report", layout="wide")

def convert_data(data):
    return data.to_csv(index=False).encode('utf-8')

uploaded_file_0 = st.file_uploader("Upload the 'NZ BSS Report' .xlsx file", key="file_uploader_0")
uploaded_file_1 = st.file_uploader("Upload the 'M10 Bronze CRC Ranking Report' .xlsm file", key="file_uploader_1")
uploaded_file_2 = st.file_uploader("Upload the 'NZ Inventory' .xlsx file", key="file_uploader_2")

if uploaded_file_0 is not None and uploaded_file_1 is not None and uploaded_file_2 is not None:
    try:
        data_BSS = pd.read_excel(uploaded_file_0, sheet_name = 'Products below safety stock')

        data_M10_ranking = pd.read_excel(uploaded_file_1, engine = 'openpyxl', sheet_name = 'Ranking',header = 5)
        data_M10_ranking = data_M10_ranking.iloc[:,4:]
        data_M10_stock = pd.read_excel(uploaded_file_1, engine = 'openpyxl', sheet_name = 'Stock',header = 2)
        data_M10_stock = data_M10_stock.iloc[:,2:]
        data_available_physical = pd.read_excel(uploaded_file_2, engine = 'openpyxl')
        
        #####################################
        
        #Working# data = pd.merge(data_BSS['Legacy'], data_M10_ranking[['Supplier Item Code', 'M10 Code','Item', 'Department', 'Range']], how='left', left_on='Legacy', right_on='Supplier Item Code')
        #Working# data = pd.merge(data, data_available_physical[['Search name','Available physical']],how='left', left_on='Legacy', right_on='Search name')
        data = pd.merge(data_available_physical[['Search name','Available physical']], data_M10_ranking[['Supplier Item Code', 'M10 Code','Item', 'Department', 'Range']], how='left', left_on='Search name', right_on='Supplier Item Code')
        data = pd.merge(data,data_BSS[['Legacy','ETA to Mondiale']], how='left', left_on='Search name', right_on='Legacy')
        
        data['SOH Status'] = ''
        
        del data['Supplier Item Code']
        
        data['Next Availabilty Date (NAVD)'] = np.where(data['ETA to Mondiale'].isna(), pd.to_datetime(date.today()) + pd.Timedelta(days=28), data['ETA to Mondiale'])
        
        data['Date item went Out of Stock'] = ''
        data['Days Out Of Stock'] = ''
        data['Mitre 10 Promo'] = ''
        data['Supplier Comments'] = ''
        
        data = pd.merge(data, data_M10_ranking[['Supplier Item Code','$Value MAT','Units MAT','SOH LW']], how='left', left_on='Search name', right_on='Supplier Item Code')
        
        del data['Supplier Item Code']
        
        data = pd.merge(data, data_M10_stock[['Supplier Item Code','WOC ']], how='left', left_on='Search name', right_on='Supplier Item Code')

        del data['Supplier Item Code']
        
        data[' '] = ''
        
        data['Physical inventory'] = data_BSS['Physical inventory']
        
        for i in ['M10 Code', '$Value MAT', 'Units MAT', 'SOH LW', 'WOC ']:
          data[i] = data[i].fillna(0).astype(int)
        
        #data = data[(data['Physical inventory']==0) & (data['M10 Code'] != 0)]
        #Working# data = data[(data['Available physical']==0) & (data['M10 Code'] != 0)]
        data = data[(data['Available physical']==0) & (data['M10 Code'] != 0)]

        remove_cols = ['Available physical', 'Legacy', 'ETA to Mondiale', ' ', 'Physical inventory']
        for col in remove_cols:
            del data[col]

        data = data.rename(columns={'Search Name': 'Supplier Sku'})

        st.dataframe(data)

        csv = convert_data(data)
        st.download_button(label="Download data as CSV", data=csv, file_name='Min_Max_with_supplier_request.csv', mime='text/csv')

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a CSV file to get started.")
