import streamlit as st
import pandas as pd

st.set_page_config(page_title="Interactive Chart", layout="wide")

uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx"])

if uploaded_file:
    try:
        headers = ['Code', 'Name']
        data = pd.read_csv(uploaded_file, header=None, names=headers) if uploaded_file.name.endswith('csv') else pd.read_excel(uploaded_file, header=None, names=headers)
        
        data.iloc[:, :2] = data.iloc[:, :2].astype(str)

        i = 0
        while not any(char.isdigit() for char in str(data.iloc[i, 0])):
            i += 1

        data = data.iloc[i:, :]
        data['Combined'] = data.iloc[:, 0] + " " + data.iloc[:, 1]

        result_string = ', '.join(data['Combined'])
        st.write(result_string)

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a file to get started.")
