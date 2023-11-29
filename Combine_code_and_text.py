import streamlit as st
import pandas as pd

st.set_page_config(page_title="Interactive Chart", layout="wide")

uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
      data = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('csv') else pd.read_excel(uploaded_file)
      
      data['Combined'] = data.iloc[:,0] + data.iloc[:,1]
      
      result_string = ', '.join(data['Combined'])
      
      st.write(result_string)

except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a file to get started.")
