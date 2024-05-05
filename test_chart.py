import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Interactive Chart", layout="wide")

uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if delimiter_check == "Yes":
            delimiter = st.sidebar.text_input('Enter delimiter')
            data = pd.read_csv(uploaded_file, delimiter=delimiter) if uploaded_file.name.endswith('csv') else pd.read_excel(uploaded_file, engine='openpyxl')
        else:
            data = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('csv') else pd.read_excel(uploaded_file, engine='openpyxl')
        st.sidebar.markdown('---')

        FM_check = st.sidebar.radio("Fill and convert N/a", ("No", "Yes"))
        st.sidebar.markdown('---')
        if FM_check == "Yes":
            data.replace('-', '', regex=True, inplace=True)
            data.replace('', 0, inplace=True)
            def convert_to_numeric(value):
                try:
                    return pd.to_numeric(value)
                except (ValueError, TypeError):
                    return value
            data = data.applymap(convert_to_numeric)
            data = data.fillna(0)        

        column_options = [str(col) for col in data.columns]

        st.dataframe(data)

        st.markdown('---')
        st.header('Grouped data')

        ##############################
        #####Filters
        ##############################

        apply_filters = st.sidebar.radio("Apply filters", ("No", "Yes"))

        st.sidebar.header("Filters")
        filter1 = st.sidebar.selectbox("Select filter:", options=column_options)
        filter1_list = [str(i) for i in data[filter1].unique()]
        filter1_list.sort()

        if apply_filters == "Yes":
            if len(filter1)>0:
                filter1_selected = st.sidebar.multiselect(filter1, options=filter1_list)
                data = data[data[filter1] == filter1_selected]
                
            if len(filter1_selected) == 0:
                filter1_selected = filter1_list

        ##############################
        #####Grouped data
        ##############################
        
        try:
            left_column, middle_column, right_column = st.columns(3)
            with left_column:
                groupby_list = [str(i) for i in data.columns]
                groupby_selected = st.multiselect("Group data by", options = groupby_list)
            with middle_column:
                groupby_data = data.groupby(by=groupby_selected).sum()
                selected_columns = st.multiselect("Selected columns", options = [str(col) for col in groupby_data.columns])
            with right_column:
                top_group = st.text_input('"+" for first x rows and "-" for last x rows"', key="top_group")
                try:
                    top_group = int(top_group)
                except:
                    if not top_group:
                        pass
                    else:
                        st.info("Please enter an integer")

            groupby_data = groupby_data[selected_columns].reset_index()
            
            groupby_data = groupby_data.sort_values(by=selected_columns[0], ascending=False)
            
            if not top_group:
                groupby_data_top = groupby_data.copy()
            elif int(top_group) > 0:
                groupby_data_top = groupby_data.head(int(top_group))
            elif int(top_group) < 0:
                groupby_data_top = groupby_data.tail(int(top_group)*-1)
            else:
                pass
            
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

        st.markdown('---')
        st.header('Chart')

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
            top_chart = st.text_input(f'"+" for first x rows and "-" for last x rows. Total lines: {len(data)}', key="top_chart")
            try:
                top_chart = int(top_chart)

                if not top_chart:
                    pass     
                elif int(top_chart) > 0:
                    data = data.head(top_chart)
                elif int(top_chart) < 0:
                    data = data.tail(top_chart*-1)
                else:
                    pass
            except:
                if ',' in top_chart:
                    data = data.iloc[int(top_chart.split(',')[0]):int(top_chart.split(',')[1])]     
                elif not top_chart:
                    pass
                else:
                    st.info("Please enter an integer")
        
        new_column_options = [str(col) for col in data.columns]

        if chart_type == "Scatter":
            x_axis = st.selectbox("Select X-axis:", options=new_column_options)
            y_axis = st.selectbox("Select Y-axis:", options=new_column_options)
            fig = px.scatter(data, x=x_axis, y=y_axis)
            
        elif chart_type == "Bar":
            x_axis = st.selectbox("Select X-axis:", options=new_column_options)
            y_axis = st.selectbox("Select Y-axis:", options=new_column_options)
            fig = px.bar(data, x=x_axis, y=y_axis)

        elif chart_type == "Line":
            x_axis = st.selectbox("Select X-axis:", options=new_column_options)
            y_axis = st.selectbox("Select Y-axis:", options=new_column_options)
            fig = px.line(data, x=x_axis, y=y_axis)
            
        elif chart_type == "Scatter Matrix":
            pd.DataFrame.iteritems = pd.DataFrame.items
            numerical_columns = data.select_dtypes(include='number').columns.tolist()
            all_numerical = st.radio("All numerical data", ("No","Yes"))
            if all_numerical == "Yes":
                dimensions = st.multiselect("Dimensions", options = new_column_options, default = numerical_columns)
            else:
                dimensions = st.multiselect("Dimensions", options = new_column_options)

            max_values = [max(data[dim])*1.1 for dim in dimensions]
            min_values = [min(data[dim]) for dim in dimensions]
            
            label_name = st.text_input('Enter data label name', key="label_name")
            
            if label_name == "":
                fig = px.scatter_matrix(data, dimensions=dimensions)
            else:
                try:
                    fig = px.scatter_matrix(data, dimensions=dimensions, color = label_name)
                except:
                    fig = px.scatter_matrix(data, dimensions=dimensions)

            for i, dim in enumerate(dimensions):
                fig.update_layout({"xaxis"+str(i+1): dict(range=[min_values[i], max_values[i]])})
                fig.update_layout({"yaxis"+str(i+1): dict(range=[min_values[i], max_values[i]])})
                
        else:
            pass
            
        fig.update_layout(height=800, width=1200, font=dict(size=8))
        st.plotly_chart(fig)
        try:
            st.dataframe(data[['Item Description'] + dimensions])
        except:
            try:
                st.dataframe(data[dimensions])
            except:
                pass

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a file to get started.")
