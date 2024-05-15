import streamlit as st
import pandas as pd

st.set_page_config(page_title="CTM report", layout="wide")

report = st.radio("Choose report supplier", ("Bunnings", "Mitre 10", "Custom"))

uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx", "xlsm"])
    
if uploaded_file is not None:

    if report == "Bunnings":
    
        try:
            data = pd.read_excel(uploaded_file, sheet_name = 'By Item', header = 5)
            data = data.iloc[:-1]
            data.columns.values[4] = 'Item Description'
    
            for i in ['Department', 'Sub Department', 'Class', 'Item Description']:
    
                st.header(f"By {i}")
                
                data_grouped1 = data.groupby(by=i).sum()[['Sales $','GP $']]
                
                total_sales = data_grouped1['Sales $'].sum()
                data_grouped1['CTS %'] = 100 * data_grouped1['Sales $'] / total_sales
                
                data_grouped1['GP %'] = data_grouped1['GP $'] / data_grouped1['Sales $']
        
                data_grouped1['CTM'] = data_grouped1['CTS %'] * data_grouped1['GP %'] / 100
        
                total_CTM = data_grouped1['CTM'].sum()
        
                data_grouped1['CTM %'] = 100 * data_grouped1['CTM'] / total_CTM
        
                data_grouped1['Check'] = data_grouped1['CTM %'] - data_grouped1['CTS %']
        
                data_grouped1 = data_grouped1.drop(columns=['GP $', 'CTM'])
                
                st.dataframe(data_grouped1.style.format(subset=["Sales $"], formatter="${:,.2f}")
                             .format(subset=["CTS %"], formatter="%{:,.2f}")
                             .format(subset=["GP %"], formatter="%{:,.2f}")
                             .format(subset=["CTM %"], formatter="%{:,.2f}")
                             .format(subset=['Check'], formatter="%{:,.2f}")
                            )
    
                st.markdown('---')
                
            st.dataframe(data)
    
        except Exception as e:
          st.error(f"An error occurred: {e}")

    elif report == "Mitre 10":
    
        try:
            data = pd.read_excel(uploaded_file, sheet_name = 'Ranking', header = 5)

            st.dataframe(data)

            data = data.rename(columns={'Item': 'Item Description'})
            data = data.rename(columns={'$Value MAT': 'Sales $'})
            data = data.rename(columns={'$GP MAT': 'GP $'})

            for i in ['SubDepartment', 'FineLine', 'Class', 'Item Description']:
    
                st.header(f"By {i}")
                
                data_grouped1 = data.groupby(by=i).sum()[['Sales $','GP $']]
                
                total_sales = data_grouped1['Sales $'].sum()
                data_grouped1['CTS %'] = 100 * data_grouped1['Sales $'] / total_sales
                
                data_grouped1['GP %'] = data_grouped1['GP $'] / data_grouped1['Sales $']
        
                data_grouped1['CTM'] = data_grouped1['CTS %'] * data_grouped1['GP %'] / 100
        
                total_CTM = data_grouped1['CTM'].sum()
        
                data_grouped1['CTM %'] = 100 * data_grouped1['CTM'] / total_CTM
        
                data_grouped1['Check'] = data_grouped1['CTM %'] - data_grouped1['CTS %']
        
                data_grouped1 = data_grouped1.drop(columns=['GP $', 'CTM'])
                
                st.dataframe(data_grouped1.style.format(subset=["Sales $"], formatter="${:,.2f}")
                             .format(subset=["CTS %"], formatter="%{:,.2f}")
                             .format(subset=["GP %"], formatter="%{:,.2f}")
                             .format(subset=["CTM %"], formatter="%{:,.2f}")
                             .format(subset=['Check'], formatter="%{:,.2f}")
                            )
    
                st.markdown('---')
                
            st.dataframe(data)

        except Exception as e:
          st.error(f"An error occurred: {e}")


    else:
        try:
            data = pd.read_excel(uploaded_file, sheet_name = 'By Item', header = 5)

        except Exception as e:
          st.error(f"An error occurred: {e}")

