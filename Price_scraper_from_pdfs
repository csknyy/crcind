import streamlit as st

uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
if uploaded_file is not None:
    df = extract_data(uploaded_file)

st.write(df)
