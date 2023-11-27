import streamlit as st
import pandas as pd

st.set_page_config(page_title="Test chart", layout="wide")

def convert_data(data):
    return data.to_csv(index=False).encode('utf-8')

uploaded_file_0 = st.file_uploader("Upload a file", key="uploaded_file_0")

if uploaded_file_0 is not None:
    try:
        try:
            data = pd.read_csv(uploaded_file_0)
        except:
            data = pd.read_excel(uploaded_file_0)

        st.dataframe(data)
        
        column_opt = [str(i) for i in data.columns]
        columns = st.multiselect("Columns", options = column_opt)

        if len(columns) == 2:
            scatter_chart = st.scatter_chart(data[columns], use_container_width=True)

            scatter_chart.set_title("Custom Scatter Chart Title")
            scatter_chart.set_xlabel(columns[0])
            scatter_chart.set_ylabel(columns[1])

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a file to get started.")
