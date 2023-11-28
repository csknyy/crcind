import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Interactive Chart", layout="wide")

uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('csv') else pd.read_excel(uploaded_file)
        column_options = [str(col) for col in data.columns]

        ###Filters
    
        '''st.sidebar.header("Filters")
        filter1 = st.sidebar.selectbox("Select filter:", options=column_options)
        
        if len(filter1)>0:
            filter1_list = [str(i) for i in data[filter1].unique()]
            filter1_list.sort()
            filter1_selected = st.sidebar.multiselect(filter1, options=filter1_list)

        if len(filter1_selected) == 0:
            filter1_selected = filter1_list
        
        data = data[data[filter1].isin(filter1_selected)]'''

        
        
        ###

        

        st.dataframe(data)

        x_axis = st.selectbox("Select X-axis:", options=column_options)
        y_axis = st.selectbox("Select Y-axis:", options=column_options)

        # Create an interactive scatter plot with Plotly Express
        fig = px.scatter(data, x=x_axis, y=y_axis, title="Interactive Scatter Plot")
        fig.update_layout(height=800, width=800)
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a file to get started.")
