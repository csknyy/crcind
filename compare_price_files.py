import pandas as pd
import streamlit as st

st.set_page_config(page_title="Compare price files", layout="wide")

def convert_df(df):
    return df.to_csv().encode('utf-8')

uploaded_files = st.file_uploader("Choose the CSV files", accept_multiple_files=True)
file_count = len(uploaded_files)

files = [f"file{i}" for i in range(int(file_count))]

i=0
for uploaded_file,file in zip(uploaded_files,files):
    file = pd.read_csv(uploaded_file)
    try:
        del file['Unnamed: 0']
    except:
        pass
    files[i] = file
    st.write("Uploaded:", uploaded_file.name)
    i = i+1

left_column0, right_column0 = st.columns(2)
with left_column0:
    st.dataframe(files[0])
with right_column0:
    st.dataframe(files[1])
        
data1 = files[0]
data2 = files[1]

data11 = data1[['Date','Customer','Legacy Item Number','Item Name','Price']]
data22 = data2[['Date','Customer','Legacy Item Number','Item Name','Price']]

merged_data = pd.merge(data11, data22, on=['Customer', 'Legacy Item Number', 'Item Name'], suffixes=('_old', '_new'))
price_increases = merged_data[merged_data['Price_new'] > merged_data['Price_old']]

price_increases['Price_old'] = pd.to_numeric(price_increases['Price_old'], errors='coerce')
price_increases['Price_new'] = pd.to_numeric(price_increases['Price_new'], errors='coerce')

price_increases.fillna(0, inplace=True)

price_increases['Price change'] = price_increases['Price_new'] - price_increases['Price_old']
price_increases['Price change %'] = (price_increases['Price change'] / price_increases['Price_old']) * 100

st.dataframe(price_increases[price_increases['Price change'] != 0])
