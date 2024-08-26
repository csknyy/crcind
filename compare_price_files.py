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

for i in range(len(files)):
    files[i].columns = files[i].columns.str.replace(' ', '_')

switch_order = st.radio("Switch order", ("No", "Yes"))
if switch_order == "No":
    data1 = files[0]
    data2 = files[1]
else:
    data1 = files[1]
    data2 = files[0]

left_column0, right_column0 = st.columns(2)
with left_column0:
    customer_opt_0 = [str(i) for i in data2["Customer"].unique()]
    customer_opt_0.sort()
    with st.expander("Select Customer"):
        customer_0 = st.multiselect("", options = customer_opt_0, default = customer_opt_0)
        if len(customer_0) == 0:
            customer_0 = [str(i) for i in data2["Customer"].unique()]

with right_column0:
    legacy_id_opt_0 = [str(i) for i in data2["Legacy_Item_Number"].unique()]
    legacy_id_opt_0.sort()
    with st.expander("Select Legacy Item Number"):
        legacy_id_0 = st.multiselect("", options = legacy_id_opt_0, default = legacy_id_opt_0)
        if len(legacy_id_0) == 0:
            legacy_id_0 = [str(i) for i in data2["Legacy_Item_Number"].unique()]

data1_temp = data1.query("Customer == @customer_0 & Legacy_Item_Number == @legacy_id_0")
data2_temp = data2.query("Customer == @customer_0 & Legacy_Item_Number == @legacy_id_0")

left_column1, right_column1 = st.columns(2)
with left_column1:
    st.dataframe(data1_temp)
with right_column1:
    st.dataframe(data2_temp)
    
st.markdown('---')

data11 = data1[['Date','Customer','Legacy_Item_Number','Item_Name','Price']]
data22 = data2[['Date','Customer','Legacy_Item_Number','Item_Name','Price']]

merged_data = pd.merge(data11, data22, on=['Customer', 'Legacy_Item_Number', 'Item_Name'], suffixes=('_old', '_new'))
merged_data['Price_old'] = pd.to_numeric(merged_data['Price_old'], errors='coerce')
merged_data['Price_new'] = pd.to_numeric(merged_data['Price_new'], errors='coerce')
#price_increases = merged_data[merged_data['Price_new'] > merged_data['Price_old']]
#price_increases['Price_old'] = pd.to_numeric(price_increases['Price_old'], errors='coerce')
#price_increases['Price_new'] = pd.to_numeric(price_increases['Price_new'], errors='coerce')
merged_data.fillna(0, inplace=True)
merged_data['Price_change'] = merged_data['Price_new'] - merged_data['Price_old']
merged_data['Price_change_%'] = (merged_data['Price_change'] / merged_data['Price_old']) * 100
merged_data = merged_data[merged_data['Price_change'] != 0]

left_column2, right_column2 = st.columns(2)
with left_column2:
    with st.expander("Select Customer"):
        customer_opt = [str(i) for i in merged_data["Customer"].unique()]
        customer_opt.sort()
        customer = st.multiselect("Customer",options = customer_opt,default=customer_opt)

with right_column2:
    with st.expander("Select Legacy Item Number"):
        legacy_id_opt = [str(i) for i in merged_data["Legacy_Item_Number"].unique()]
        legacy_id_opt.sort()
        legacy_id = st.multiselect("Legacy Item Number",options = legacy_id_opt,default=legacy_id_opt)

merged_data = merged_data.query("Customer == @customer & Legacy_Item_Number == @legacy_id")

st.dataframe(merged_data)
