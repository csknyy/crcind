import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Interactive Chart", layout="wide")

uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('csv') else pd.read_excel(uploaded_file)
        column_options = [str(col) for col in data.columns]

        st.dataframe(data)

        ##############################
        #####Filters
        ##############################

        apply_filters = st.sidebar.radio("Apply filters", ("No", "Yes"))
    
        st.sidebar.header("Filters")
        filter1 = st.sidebar.selectbox("Select filter:", options=column_options)
        
        if len(filter1)>0:
            filter1_list = [str(i) for i in data[filter1].unique()]
            filter1_list.sort()
            filter1_selected = st.sidebar.multiselect(filter1, options=filter1_list)

        if len(filter1_selected) == 0:
            filter1_selected = filter1_list

        if apply_filters == "Yes":
            data = data[data[filter1].isin(filter1_selected)]

        ##############################
        #####Groupby
        ##############################
        
        try:
            left_column, middle_column, right_column = st.columns(3)
            with left_column:
                groupby_list = [str(i) for i in data.columns]
                groupby_selected = st.multiselect("Group by", options = column_options)
            with middle_column:
                groupby_data = data.groupby(by=groupby_selected).sum()
                selected_columns = st.multiselect("Selected columns", options = [str(col) for col in groupby_data.columns])
            with right_column:
                pass
    
            groupby_data = groupby_data[selected_columns]
            st.dataframe(groupby_data)
    
            #groupby_list = [str(i) for i in data.columns]
            #groupby_selected = st.multiselect("Group by", options = column_options)
            #if len(groupby_selected) != 0:
            #    groupby_data = data.groupby(by=groupby_selected).sum()
            #    selected_columns = st.multiselect("Selected columns", options = [str(col) for col in groupby_data.columns])
            #    groupby_data = groupby_data[selected_columns]
            #    st.dataframe(groupby_data)
        except:
            pass
        
        ##############################

        data_type = st.radio("", ("Raw data", "Grouped data"))

        if data_type == "Raw data":
            data = data
        else:
            data = groupby_data

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
