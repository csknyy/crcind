import streamlit as st
import pandas as pd

st.set_page_config(page_title="Open orders report", layout="wide")

def convert_data(data):
    return data.to_csv(index=False).encode('utf-8')

uploaded_file_0 = st.file_uploader("Upload the Picking list registration report from D3FO", key="file_uploader_0")
uploaded_file_1 = st.file_uploader("Upload the Open Orders (SKU) report from Power BI ", key="file_uploader_1")

if uploaded_file_0 is not None and uploaded_file_1 is not None:
    try:
        D3FO = pd.read_excel(uploaded_file_0, header=0)

        PowerBI = pd.read_excel(uploaded_file_1, header=2)

        D3FO = D3FO[D3FO["Handling status"] == "Activated"]

        data = PowerBI.groupby(D3FO["Number"])[["Open Ordered $", "Open Qty"]].sum().sort_values(by="Open Ordered $", ascending=False)
        
        data = data[data["Open Ordered $"] != 0]

        st.dataframe(data)

        csv = convert_data(data)
        st.download_button(label="Download data as CSV", data=csv, file_name='Min_Max_with_supplier_request.csv', mime='text/csv')

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload the reports to get started.")
