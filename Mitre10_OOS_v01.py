import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mitre 10 OOS report", layout="wide")

def convert_data(data):
    return data.to_csv(index=False).encode('utf-8')

uploaded_file_0 = st.file_uploader("Upload the 'NZ BSS Report' .xlsx file", key="file_uploader_0")
uploaded_file_1 = st.file_uploader("Upload the 'M10 Bronze CRC Ranking Report' .xlsm file", key="file_uploader_1")
uploaded_file_2 = st.file_uploader("For Bryce - Upload the rolling 12 month sales data for Mitre10 NZ using the financial year report", key="file_uploader_2")
uploaded_file_3 = st.file_uploader("For Bryce - Upload the rolling 12 month sales data for all NZ using the financial year report", key="file_uploader_3")
uploaded_file_4 = st.file_uploader("For Martin - Upload the rolling 12 month sales data for Bunnings NZ using the financial year report", key="file_uploader_4")

if uploaded_file_0 is not None and uploaded_file_1 is not None and uploaded_file_2 is not None and uploaded_file_3:
    try:
        data_BSS = pd.read_excel(uploaded_file_0, sheet_name='Products below safety stock')
    
        data_M10_ranking = pd.read_excel(uploaded_file_1, engine='openpyxl', sheet_name='Ranking', header=5)
        data_M10_ranking = data_M10_ranking.iloc[:, 4:]
        data_M10_stock = pd.read_excel(uploaded_file_1, engine='openpyxl', sheet_name='Stock', header=2)
        data_M10_stock = data_M10_stock.iloc[:, 2:]
    
        #####################################
    
        data = pd.merge(data_BSS['Legacy'], data_M10_ranking[['Supplier Item Code', 'M10 Code', 'Item', 'Department', 'Range']], how='left', left_on='Legacy', right_on='Supplier Item Code')
    
        data['SOH Status'] = ''
    
        del data['Supplier Item Code']
    
        data['Next Availabilty Date (NAVD)'] = data_BSS['ETA to Mondiale']
    
        data['Date item went Out of Stock'] = ''
        data['Days Out Of Stock'] = ''
        data['Mitre 10 Promo'] = ''
        data['Supplier Comments'] = ''
    
        data = pd.merge(data, data_M10_ranking[['Supplier Item Code', '$Value MAT', 'Units MAT', 'SOH LW']], how='left', left_on='Legacy', right_on='Supplier Item Code')
    
        del data['Supplier Item Code']
    
        data = pd.merge(data, data_M10_stock[['Supplier Item Code', 'WOC ']], how='left', left_on='Legacy', right_on='Supplier Item Code')
    
        del data['Supplier Item Code']
    
        data[' '] = ''
    
        data['Physical inventory'] = data_BSS['Physical inventory']
    
        for i in ['M10 Code', '$Value MAT', 'Units MAT', 'SOH LW', 'WOC ']:
            data[i] = data[i].fillna(0).astype(int)
    
        data = data[(data['Physical inventory'] == 0) & (data['M10 Code'] != 0)]
    
        del data['Physical inventory']
        del data[' ']
    
        st.dataframe(data)
    
        #st.markdown('---')
    
        #farm_source_article = ['204902', '205186', '205351', '205876', '210467', '223155', '262830', '262831', '262832', '264292', '265170', '264285', '264287', '265747', '265761', '223157', '205874', '205875', '250603', '264932', '223295']
        #farm_source_items = ['5040', '3055', '5035', '2091', '5070', '5089', '1751846', '1751837', '8498', '1751839', '1753211', 'EVR1', 'EVR5', '1753427', '1754785', '8017', '2087', '2089', '2125', '1753336', '5911']
        #farm_source_item_names = ['Lubricant Engine Start CRC 400mL', 'Lubricant 808 Silicone Spray CRC 500mL', 'Lubricant Tac 2 CRC 300g', 'Lubricant Prime It CRC 400mL', 'Degreaser Aeroclean 500ml', 'Degreaser Brakleen CRC 600g', 'Lubricant 556 CRC 4L', 'Lubricant Aerosol 556 CRC 420ml', 'Spray Seal Leak Stop 350gm', 'Lubricant 556 CRC Marine 420ml', 'Lubricant 808 Silicone 15% Extra 575ml', 'Lubricant Evapo-Rust 1L', 'Lubricant Evapo-Rust 5L', 'Cleaner Solar Panel WattsUp Conc 5L', 'Cleaner Solar Panel WattsUp Conc 1L', 'Adhesive Spray F2 Multipurpose 575mL', 'Paint Zinc Bright CRC 400mL', 'Paint Zinc Black CRC 400mL', 'Spray CRC Zinc It 500gm', 'Spray Evapo-Rust Gel CRC 500g', 'Fungicide Clene Up Slow Release CRC 5L']
    
        #farm_source_map = pd.DataFrame()
        #farm_source_map['Article Vendor'] = farm_source_article
        #farm_source_map['Vendor Article Number'] = farm_source_items
        #farm_source_map['Description'] = farm_source_item_names
    
        #farm_source_data = data_BSS[data_BSS['Legacy'].isin(farm_source_items)]
    
        #merged_data = pd.merge(farm_source_map, farm_source_data, left_on='Vendor Article Number', right_on='Legacy', how='inner')
        #merged_data = merged_data[['Article Vendor', 'Vendor Article Number', 'Description', 'ETA to Mondiale', 'Comments']]
        #merged_data = merged_data.rename(columns={'ETA to Mondiale': 'ETA'})
        
        #st.dataframe(merged_data)
    
        st.markdown('---')
    
        all_NZ_data = pd.read_excel(uploaded_file_3, engine='openpyxl', header=2)
        all_NZ_data = all_NZ_data.iloc[:,[0,1,2,11]]
        all_NZ_data['All NZ Avg'] = round(all_NZ_data.iloc[:,-1] / 12, 0)
        all_NZ_data = all_NZ_data.rename(columns={'Item Number': 'Item number'})
    
        all_M10_data = pd.read_excel(uploaded_file_2, engine='openpyxl', header=2)
        all_M10_data = all_M10_data.iloc[:,[0,1,2,11]]
        all_M10_data['Mitre 10 Avg'] = round(all_M10_data.iloc[:,-1] / 12, 0)
        all_M10_data = all_M10_data.rename(columns={'Item Number': 'Item number'})

        all_Bunnings_data = pd.read_excel(uploaded_file_4, engine='openpyxl', header=2)
        all_Bunnings_data = all_Bunnings_data.iloc[:,[0,1,2,11]]
        all_Bunnings_data['Bunnings Avg'] = round(all_Bunnings_data.iloc[:,-1] / 12, 0)
        all_Bunnings_data = all_Bunnings_data.rename(columns={'Item Number': 'Item number'})

    
    
        merged_sales_data = pd.merge(data_BSS, all_NZ_data[['Item number', 'All NZ Avg']], on='Item number', how='left')
        data_BSS['All NZ Avg'] = merged_sales_data['All NZ Avg']
    
        merged_sales_data = pd.merge(data_BSS, all_M10_data[['Item number', 'Mitre 10 Avg']], on='Item number', how='left')
        data_BSS['Mitre 10 Avg'] = merged_sales_data['Mitre 10 Avg']

        merged_sales_data = pd.merge(data_BSS, all_Bunnings_data[['Item number', 'Bunnings Avg']], on='Item number', how='left')
        data_BSS['Bunnings Avg'] = merged_sales_data['Bunnings Avg']
    
        st.dataframe(data_BSS)

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a CSV file to get started.")
