import streamlit as st
import pandas as pd

st.set_page_config(page_title="CTM report", layout="wide")

report = st.radio("Choose report supplier", ("Bunnings", "Mitre 10", "Custom"))
    
if report == "Bunnings":

    uploaded_file = st.file_uploader("Upload a Bunnings KPI report", type=["csv", "xlsx", "xlsm"])
    if uploaded_file is not None:
    
        try:
            data = pd.read_excel(uploaded_file, sheet_name = 'By Item', header = 5)
            data = data.iloc[:-1]
            data.columns.values[4] = 'Item Description'
    
            for i in ['Department', 'Sub Department', 'Class', 'Item Description']:
    
                st.header(f"By {i}")
                
                data_grouped1 = data.groupby(by=i).sum()[['Sales $','GP $']]
                
                total_sales = data_grouped1['Sales $'].sum()
                data_grouped1['CTS %'] = 100 * data_grouped1['Sales $'] / total_sales
                
                data_grouped1['GP %'] = 100*data_grouped1['GP $'] / data_grouped1['Sales $']
        
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

    uploaded_file = st.file_uploader("Upload a Mitre 10 Bronze CRC trade ranking report", type=["csv", "xlsx", "xlsm"])
    if uploaded_file is not None:
           
        try:
            data = pd.read_excel(uploaded_file, sheet_name = 'Ranking', header = 5)

            data = data.rename(columns={'Item': 'Item Description'})
            data = data.rename(columns={'$Value MAT': 'Sales $'})
            data = data.rename(columns={'Units MAT': 'Units'})
            data = data.rename(columns={'$GP MAT': 'GP $'})

            data2 = data[['Department', 'SubDepartment', 'FineLine', 'Item Description', 'Sales $', 'Units', 'GP $']]

            for i in ['SubDepartment', 'FineLine', 'Item Description']:
    
                st.header(f"By {i}")
                
                data_grouped1 = data2.groupby(by=i).sum()[['Sales $','Units','GP $']]
                
                total_sales = data_grouped1['Sales $'].sum()

                data_grouped1['Avg Price'] = data_grouped1['Sales $'] / data_grouped1['Units']
                
                data_grouped1['CTS %'] = 100 * data_grouped1['Sales $'] / total_sales
                
                data_grouped1['GP %'] = 100 * data_grouped1['GP $'] / data_grouped1['Sales $']
        
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
    left_column0, middle_column0, right_column0 = st.columns(3)
    with left_column0:
        sheetname = st.text_input("Enter prefered sheet name")
    with middle_column0:
        header_ind = st.text_input("Enter prefered header index")
        try:
            header_ind = int(header_ind) - 1
        except:
            pass
    with right_column0:
        pass

    uploaded_file = st.file_uploader("Upload a file")
    
    if uploaded_file is not None:
        
        try:
            if len(sheetname)>0 and header_ind>0:
                data = pd.read_excel(uploaded_file, sheet_name = sheetname, header = header_ind)
            elif len(sheetname)>0:
                data = pd.read_excel(uploaded_file, sheet_name = sheetname)
            elif header_ind>0:
                data = pd.read_excel(uploaded_file, header = header_ind)
            else:
                data = pd.read_excel(uploaded_file)

            column_names = data.columns

            left_column0, middle_column0, right_column0 = st.columns(3)
            with left_column0:
                item_description = st.selectbox("Select item description", options = column_names, key = "text0")
            with middle_column0:
                sales_data = st.selectbox("Select Sales $", options = column_names, key = "text1")
            with right_column0:
                GP_data =  st.selectbox("Select GP $", options = column_names, key = "text2")
            
            data2 = data.copy()

            selected_columns = [item_description, sales_data, GP_data]
            groupby_columns = st.multiselect("Select columns to group by", options = column_names)
            for i in groupby_columns:
                selected_columns.append(i)

            selected_columns = set(i for i in selected_columns)
            selected_columns = [i for i in selected_columns]

            data2 = data2[selected_columns]

            #data2 = data2.rename(columns={item_description : 'Item Description'})
            data2 = data2.rename(columns={sales_data : 'Sales $'})
            data2 = data2.rename(columns={GP_data : 'GP $'})

            for i in groupby_columns:
            #for i in ['Item Description']:
    
                st.header(f"By {i}")
                
                data_grouped1 = data2.groupby(by=i).sum()[['Sales $','GP $']]
                
                total_sales = data_grouped1['Sales $'].sum()
                data_grouped1['CTS %'] = 100 * data_grouped1['Sales $'] / total_sales
                
                data_grouped1['GP %'] = 100 * data_grouped1['GP $'] / data_grouped1['Sales $']
        
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

