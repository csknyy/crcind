import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mitre 10 missing items", layout="wide")

uploaded_file = st.file_uploader("Upload a file")

if uploaded_file is not None:
  try:  
    data = pd.read_excel(uploaded_file, sheet_name="RangeGaps", header = 1)
    st.dataframe(data)

  except:
    st.error(f"An error occurred: {e}")
