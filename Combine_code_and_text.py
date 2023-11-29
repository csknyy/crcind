import streamlit as st
import pandas as pd

st.set_page_config(page_title="Interactive Chart", layout="wide")

uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:

        headers = ['Code', 'Name']        
        data = pd.read_csv(uploaded_file, header=None, names=headers) if uploaded_file.name.endswith('csv') else pd.read_excel(uploaded_file, header=None, names=headers)
        
        data['Code'] = [str(i).split('.')[0] for i in data['Code']]
        data['Name'] = [str(i) for i in data['Name']]
        
        ########################################
        ########################################
        def contains_number(s):
            return any(char.isdigit() for char in s)

        i = 0
        check = False
        while check == False:
            for cell in data['Code']:
              check = contains_number(str(cell))
              i =+ 1
        
        data = data.iloc[i:,:]
        ########################################
        ########################################
        
        data['Combined'] = data.iloc[:,0] + " " + data.iloc[:,1]
        
        result_string = ', '.join(data['Combined'])
        
        st.write(result_string)
    
    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a file to get started.")
