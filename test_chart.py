import streamlit as st
import pandas as pd

st.set_page_config(page_title="Test chart", layout="wide")

def convert_data(data):
    return data.to_csv(index=False).encode('utf-8')

data = st.file_uploader("Upload a file", key="data")

if data is not None:
    try:
        column_opt = [str(i) for i in data.columns]
        column = st.multiselect("Column", options = column_opt)

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a file to get started.")
