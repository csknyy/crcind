import streamlit as st

st.set_page_config(page_title="Price Scraper", layout="wide")

def convert_data(data):
    return data.to_csv(index=False).encode('utf-8')

uploaded_file_0 = st.file_uploader("Upload a file", key="file_uploader_0")

if uploaded_file_0 is not None and uploaded_file_1 is not None:
    try:
        pass

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a file to get started.")
