import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mitre 10 OOS report", layout="wide")

def convert_data(data):
    return data.to_csv(index=False).encode('utf-8')

uploaded_file_0 = st.file_uploader("Upload the 'NZ BSS Report' .xlsx file", key="file_uploader_0")

# Radio button to decide if uploaded_file_1 is required
use_m10_ranking = st.radio(
    "Do you want to include the 'M10 Bronze CRC Ranking Report'?",
    ("Yes", "No"),
    key="m10_ranking_option"
)

uploaded_file_1 = None
if use_m10_ranking == "Yes":
    uploaded_file_1 = st.file_uploader("Upload the 'M10 Bronze CRC Ranking Report' .xlsm file", key="file_uploader_1")

uploaded_file_2 = st.file_uploader("For Bryce - Upload the rolling 12 month sales data for Mitre10 NZ using the financial year report", key="file_uploader_2")
uploaded_file_3 = st.file_uploader("For Bryce - Upload the rolling 12 month sales data for all NZ using the financial year report", key="file_uploader_3")
uploaded_file_4 = st.file_uploader("For Martin - Upload the rolling 12 month sales data for Bunnings NZ using the financial year report", key="file_uploader_4")

# Check if essential files are uploaded, and handle optional file based on radio button
if uploaded_file_0 is not None and uploaded_file_2 is not None and uploaded_file_3 is not None and uploaded_file_4 is not None:
    # If M10 ranking is chosen, ensure the file is uploaded
    if use_m10_ranking == "Yes" and uploaded_file_1 is None:
        st.info("Please upload the 'M10 Bronze CRC Ranking Report' or select 'No' to bypass it.")
    else:
        try:
            data_BSS = pd.read_excel(uploaded_file_0, sheet_name='Products below safety stock')
            
            data_M10_ranking = pd.DataFrame() # Initialize as empty
            data_M10_stock = pd.DataFrame()   # Initialize as empty

            if use_m10_ranking == "Yes" and uploaded_file_1 is not None:
                data_M10_ranking = pd.read_excel(uploaded_file_1, engine='openpyxl', sheet_name='Ranking', header=5)
                data_M10_ranking = data_M10_ranking.iloc[:, 4:]
                data_M10_stock = pd.read_excel(uploaded_file_1, engine='openpyxl', sheet_name='Stock', header=2)
                data_M10_stock = data_M10_stock.iloc[:, 2:]
            
            #####################################
            
            # Conditionally merge based on whether data_M10_ranking was loaded
            if not data_M10_ranking.empty:
                data = pd.merge(data_BSS['Legacy'], data_M10_ranking[['Supplier Item Code', 'M10 Code', 'Item', 'Department', 'Range']], how='left', left_on='Legacy', right_on='Supplier Item Code')
            else:
                # If no M10 ranking file, initialize 'data' with 'Legacy' column and other required columns with NaNs
                data = pd.DataFrame({'Legacy': data_BSS['Legacy'].unique()})
                for col in ['M10 Code', 'Item', 'Department', 'Range']:
                    data[col] = pd.NA # Or you can use '' depending on your preference for missing data
            
            data['SOH Status'] = ''
            
            if 'Supplier Item Code' in data.columns:
                del data['Supplier Item Code']
            
            data['Next Availabilty Date (NAVD)'] = data_BSS['ETA to Mondiale']
            
            data['Date item went Out of Stock'] = ''
            data['Days Out Of Stock'] = ''
            data['Mitre 10 Promo'] = ''
            data['Supplier Comments'] = ''
            
            if not data_M10_ranking.empty:
                data = pd.merge(data, data_M10_ranking[['Supplier Item Code', '$Value MAT', 'Units MAT', 'SOH LW']], how='left', left_on='Legacy', right_on='Supplier Item Code')
            else:
                for col in ['$Value MAT', 'Units MAT', 'SOH LW']:
                    data[col] = pd.NA
            
            if 'Supplier Item Code' in data.columns:
                del data['Supplier Item Code']
            
            if not data_M10_stock.empty:
                data = pd.merge(data, data_M10_stock[['Supplier Item Code', 'WOC ']], how='left', left_on='Legacy', right_on='Supplier Item Code')
            else:
                data['WOC '] = pd.NA
            
            if 'Supplier Item Code' in data.columns:
                del data['Supplier Item Code']
            
            data[' '] = ''
            
            data['Physical inventory'] = data_BSS['Physical inventory']
            
            for i in ['M10 Code', '$Value MAT', 'Units MAT', 'SOH LW', 'WOC ']:
                if i in data.columns:
                    data[i] = data[i].fillna(0).astype(int)
            
            data = data[(data['Physical inventory'] == 0) & (data['M10 Code'] != 0)]
            
            del data['Physical inventory']
            del data[' ']
            
            st.dataframe(data)
            
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
    st.info("Please upload the required files to get started.")
