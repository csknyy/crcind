import streamlit as st
import pandas as pd

st.set_page_config(page_title="Open orders report", layout="wide")

def convert_data(data):
    return data.to_csv(index=False).encode('utf-8')

uploaded_file_0 = st.file_uploader("Upload the Picking list registration report from D3FO", key="file_uploader_0")
uploaded_file_1 = st.file_uploader("Upload the Open Orders by Order Creation Date report from Power BI ", key="file_uploader_1")

if uploaded_file_0 is not None and uploaded_file_1 is not None:
    try:
        D3FO = pd.read_excel(uploaded_file_0, header=0)

        PowerBI = pd.read_excel(uploaded_file_1, header=2)

        D3FO = D3FO[D3FO["Handling status"] == "Activated"]

        D3FO['Number'] = [str(i) for i in D3FO['Number']]

        data = PowerBI[PowerBI['Sales Order Number'].isin(D3FO['Number'])][["Sales Order Number", "Open Ordered $", "Open Qty"]].groupby(by='Sales Order Number').sum().sort_values(by="Open Ordered $", ascending=False)
        data.index.rename('Sales Order Number', inplace=True)
        data = data.reset_index()

        st.header(f'Total value: ${data["Open Ordered $"].sum():,.2f}')
        st.subheader(f'Total lines: {len(data["Open Ordered $"])}')
        st.subheader(f'Total qty: {data["Open Qty"].sum():,.0f}')

        data2 = PowerBI[PowerBI['Sales Order Number'].isin(D3FO['Number'])][["Item Description", "Open Ordered $", "Open Qty"]].groupby(by='Item Description').sum().sort_values(by="Open Ordered $", ascending=False)
        data2.index.rename('Item Description', inplace=True)
        data2 = data2.reset_index()


        col1, col2 = st.columns(2)

        with col1:
            #st.dataframe(data.style.format(subset=["Open Ordered $"], formatter="${:,.2f}").format(subset=["Sales Order Number"], formatter="{:.0f}"))
            st.dataframe(data.style.format(subset=["Open Ordered $"], formatter="${:,.2f}").format(subset=["Open Qty"], formatter="{:,.0f}"))
    
            #csv = convert_data(data)
            #st.download_button(label="Download data as CSV", data=csv, file_name='open_orders_report.csv', mime='text/csv')

        with col2:
            st.dataframe(data2.style.format(subset=["Open Ordered $"], formatter="${:,.2f}").format(subset=["Open Qty"], formatter="{:,.0f}"))
            

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload the reports to get started.")
