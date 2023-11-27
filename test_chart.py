"""import streamlit as st
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
            #st.scatter_chart(data[columns])
            
            x_axis = st.selectbox("X-axis", columns)
            y_axis = st.selectbox("Y-axis", columns)
            st.scatter_chart(data, x=x_axis, y=y_axis)

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a file to get started.")"""

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Interactive Chart", layout="wide")

uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('csv') else pd.read_excel(uploaded_file)

        st.dataframe(data)

        column_options = [str(col) for col in data.columns]
        x_axis = st.selectbox("Select X-axis:", options=column_options)
        y_axis = st.selectbox("Select Y-axis:", options=column_options)

        # Create an interactive scatter plot with Plotly Express
        fig = px.scatter(data, x=x_axis, y=y_axis, title="Interactive Scatter Plot")
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a file to get started.")
