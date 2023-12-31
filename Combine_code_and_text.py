import streamlit as st
import pandas as pd

st.set_page_config(page_title="Interactive Chart", layout="wide")

uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:

        headers = ['Code', 'Name']        
        data = pd.read_csv(uploaded_file, header=None, names=headers) if uploaded_file.name.endswith('csv') else pd.read_excel(uploaded_file, header=None, names=headers)
        
        data = data.dropna()

        data['Code'] = [str(int(i)) for i in data['Code']]
        data['Name'] = [str(i) for i in data['Name']]
        
        ########################################
        ########################################
        def contains_number(s):
            return any(char.isdigit() for char in s)
        
        slice = next((index for index, cell in enumerate(data['Code']) if contains_number(str(cell))), len(data['Code']))
        
        data = data.iloc[slice:,:]
        ########################################
        ########################################
        
        data['Combined'] = data.iloc[:,0] + " " + data.iloc[:,1]
        
        result_string = ', '.join(data['Combined'])

        st.write(result_string)
    
    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a file to get started.")
