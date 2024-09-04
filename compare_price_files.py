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

data1['Price'] = pd.to_numeric(data1['Price'], errors='coerce')
data2['Price'] = pd.to_numeric(data2['Price'], errors='coerce')

left_column0, middle_column0, right_column0 = st.columns(3)
with left_column0:
    country_opt_0 = [str(i) for i in data2["Country"].unique()]
    country_opt_0.sort()
    with st.expander("Select Country"):
        country_0 = st.multiselect("", options = country_opt_0, default = country_opt_0)
        if len(country_0) == 0:
            country_0 = [str(i) for i in data2["Country"].unique()]

with middle_column0:
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
        legacy_id_0 = st.multiselect("", options = legacy_id_opt_0, default = [])
        if len(legacy_id_0) == 0:
            legacy_id_0 = [str(i) for i in data2["Legacy_Item_Number"].unique()]

data1_temp = data1.query("Country == @country_0 & Customer == @customer_0 & Legacy_Item_Number == @legacy_id_0")
data2_temp = data2.query("Country == @country_0 & Customer == @customer_0 & Legacy_Item_Number == @legacy_id_0")

left_column1, right_column1 = st.columns(2)
with left_column1:
    st.dataframe(data1_temp)
with right_column1:
    st.dataframe(data2_temp)
    
st.markdown('---')

data11 = data1[['Date','Country','Customer','Legacy_Item_Number','Item_Name','Price']]
data22 = data2[['Date','Country','Customer','Legacy_Item_Number','Item_Name','Price']]

merged_data = pd.merge(data11, data22, on=['Country','Customer', 'Legacy_Item_Number', 'Item_Name'], suffixes=('_old', '_new'))
merged_data.fillna(0, inplace=True)
merged_data['Price_change'] = round(merged_data['Price_new'] - merged_data['Price_old'],2)
merged_data['Price_change_%'] = round(100 * merged_data['Price_change'] / merged_data['Price_old'],2)
merged_data = merged_data[merged_data['Price_change'] != 0]

cheapest_prices = data22.groupby(['Country','Legacy_Item_Number',])['Price'].min().reset_index()
merged_data = pd.merge(merged_data, cheapest_prices, on=['Country', 'Legacy_Item_Number'], how='left', suffixes=('', '_cheapest'))
merged_data.rename(columns={'Price': 'Cheapest_price'}, inplace=True)
merged_data['Cheapest'] = ['Cheap' if price_new == cheapest_price else '' for price_new, cheapest_price in zip(merged_data['Price_new'], merged_data['Cheapest_Price'])]
st.dataframe(cheapest_prices)

left_column2, middle_column2, right_column2 = st.columns(3)
with left_column2:
    with st.expander("Select Country"):
        country_opt = [str(i) for i in merged_data["Country"].unique()]
        country_opt.sort()
        country = st.multiselect("Country", options = country_opt, default = country_opt)
        if len(country) == 0:
            country = [str(i) for i in merged_data["Country"].unique()]

with middle_column2:
    with st.expander("Select Customer"):
        customer_opt = [str(i) for i in merged_data["Customer"].unique()]
        customer_opt.sort()
        customer = st.multiselect("Customer",options = customer_opt,default=customer_opt)
        if len(customer) == 0:
            customer = [str(i) for i in merged_data["Customer"].unique()]

with right_column2:
    with st.expander("Select Legacy Item Number"):
        legacy_id_opt = [str(i) for i in merged_data["Legacy_Item_Number"].unique()]
        legacy_id_opt.sort()
        legacy_id = st.multiselect("Legacy Item Number",options = legacy_id_opt,default=legacy_id_opt)
        if len(legacy_id) == 0:
            legacy_id = [str(i) for i in merged_data["Legacy_Item_Number"].unique()]

merged_data = merged_data.query("Country == @country & Customer == @customer & Legacy_Item_Number == @legacy_id")

st.dataframe(merged_data)
