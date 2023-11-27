import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Test chart", layout="wide")

uploaded_file_0 = st.file_uploader("Upload a file", key="uploaded_file_0")

if uploaded_file_0 is not None:
    try:
        try:
            data = pd.read_csv(uploaded_file_0)
        except:
            data = pd.read_excel(uploaded_file_0)

        st.dataframe(data)
        
        column_opt = [str(i) for i in data.columns]
        columns = st.multiselect("Columns", options=column_opt)

        if len(columns) == 2:
            fig, ax = plt.subplots()
            ax.scatter(data[columns[0]], data[columns[1]])
            ax.set_xlabel(columns[0])
            ax.set_ylabel(columns[1])
            ax.set_title('Scatter Chart')

            st.pyplot(fig)

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a file to get started.")
