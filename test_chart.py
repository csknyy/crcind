import streamlit as st

st.set_page_config(page_title="Test chart", layout="wide")

def convert_data(data):
    return data.to_csv(index=False).encode('utf-8')

data = st.file_uploader("Upload a file", key="file_uploader_0")

if data is not None:
    try:
        category = st.multiselect("Category", options=category_opt)
        supplier_opt = [str(i) for i in data["Supplier"].unique()]

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a file to get started.")