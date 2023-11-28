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
                top_group = st.text_input("Top x rows:", key="top_group")
                bottom_group = st.text_input("Bottom x rows:", key="bottom_group")
    
            groupby_data = groupby_data[selected_columns].sort_values(by=selected_columns[0], ascending=False)
            groupby_data = groupby_data.reset_index()

            if not top_group and not bottom_group:
                pass
            elif int(top_group) > 0:
                groupby_data_top = groupby_data.head(int(top_group))
            elif int(bottom_group) > 0:
                groupby_data_top = groupby_data.tail(int(bottom_group))
            else:
                groupby_data_top = groupby_data.copy()
            
            st.dataframe(groupby_data_top)
    
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

        left_column, middle_column, right_column = st.columns(3)
        with left_column:
            data_type = st.radio("", ("Raw data", "Grouped data"))

            if data_type == "Raw data":
                data = data
            else:
                data = groupby_data
            
        with middle_column:
            chart_type = st.radio("", ("Scatter", "Scatter Matrix", "Line", "Bar"))
        with right_column:
            top_chart = st.text_input("Enter your text here:", key = "top_chart")
            bottom_chart = st.text_input("Enter your text here:", key = "bottom_chart")

        if not top_chart and not bottom_chart:
            pass
        elif int(top_chart) > 0:
            data = data.head(int(top_chart))
        elif int(bottom_chart) > 0:
            data = data.tail(int(bottom_chart))
        else:
            pass
        
        new_column_options = [str(col) for col in data.columns]

        if chart_type == "Scatter":
            x_axis = st.selectbox("Select X-axis:", options=new_column_options)
            y_axis = st.selectbox("Select Y-axis:", options=new_column_options)
    
            fig = px.scatter(data, x=x_axis, y=y_axis)
            fig.update_layout(height=800, width=800)
            st.plotly_chart(fig)
            
        elif chart_type == "Scatter Matrix":
            dimensionss = st.multiselect("Dimensions", options = new_column_options)
            fig = px.scatter_matrix(data, dimensions = dimensionss)
            st.plotly_chart(fig)
        
        elif chart_type == "Bar":
            x_axis = st.selectbox("Select X-axis:", options=new_column_options)
            y_axis = st.selectbox("Select Y-axis:", options=new_column_options)

            fig = px.bar(data, x=x_axis, y=y_axis)
            fig.update_layout(height=800, width=800)
            st.plotly_chart(fig)

        elif chart_type == "Line":
            x_axis = st.selectbox("Select X-axis:", options=new_column_options)
            y_axis = st.selectbox("Select Y-axis:", options=new_column_options)

            fig = px.line(data, x=x_axis, y=y_axis)
            fig.update_layout(height=800, width=800)
            st.plotly_chart(fig)

        else:
            pass

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a file to get started.")
