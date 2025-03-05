import streamlit as st
import pandas as pd

st.set_page_config(page_title="Farm Source OOS report", layout="wide")

uploaded_file_0 = st.file_uploader("Upload the 'NZ BSS Report' .xlsx file", key="file_uploader_0")
if uploaded_file_0 is not None:
  try:
    data_BSS = pd.read_excel(uploaded_file_0, sheet_name='Products below safety stock')
    
    farm_source_article = ['204902', '205186', '205351', '205876', '210467', '223155', '262830', '262831', '262832', '264292', '265170', '264285', '264287', '265747', '265761', '223157', '205874', '205875', '250603', '264932', '223295']
    farm_source_items = ['5040', '3055', '5035', '2091', '5070', '5089', '1751846', '1751837', '8498', '1751839', '1753211', 'EVR1', 'EVR5', '1753427', '1754785', '8017', '2087', '2089', '2125', '1753336', '5911']
    farm_source_item_names = ['Lubricant Engine Start CRC 400mL', 'Lubricant 808 Silicone Spray CRC 500mL', 'Lubricant Tac 2 CRC 300g', 'Lubricant Prime It CRC 400mL', 'Degreaser Aeroclean 500ml', 'Degreaser Brakleen CRC 600g', 'Lubricant 556 CRC 4L', 'Lubricant Aerosol 556 CRC 420ml', 'Spray Seal Leak Stop 350gm', 'Lubricant 556 CRC Marine 420ml', 'Lubricant 808 Silicone 15% Extra 575ml', 'Lubricant Evapo-Rust 1L', 'Lubricant Evapo-Rust 5L', 'Cleaner Solar Panel WattsUp Conc 5L', 'Cleaner Solar Panel WattsUp Conc 1L', 'Adhesive Spray F2 Multipurpose 575mL', 'Paint Zinc Bright CRC 400mL', 'Paint Zinc Black CRC 400mL', 'Spray CRC Zinc It 500gm', 'Spray Evapo-Rust Gel CRC 500g', 'Fungicide Clene Up Slow Release CRC 5L']

    farm_source_map = pd.DataFrame()
    farm_source_map['Article Vendor'] = farm_source_article
    farm_source_map['Vendor Article Number'] = farm_source_items
    farm_source_map['Description'] = farm_source_item_names

    farm_source_data = data_BSS[data_BSS['Legacy'].isin(farm_source_items)]
    
    merged_data = pd.merge(farm_source_map, farm_source_data, left_on='Vendor Article Number', right_on='Legacy', how='inner')
    merged_data = merged_data[['Article Vendor', 'Vendor Article Number', 'Description', 'ETA to Mondiale', 'Comments']]
    merged_data = merged_data.rename(columns={'ETA to Mondiale': 'ETA'})
    
    st.dataframe(merged_data)

  except Exception as e:
    st.error(f"An error occurred: {e}")

else:
    st.info("Please upload the BSS file to get started.")
