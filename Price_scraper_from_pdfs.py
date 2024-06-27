import streamlit as st

uploaded_file = st.file_uploader("Choose your .pdf file", type="pdf")

pdf_data = open(uploaded_file, "rb").read()

st.write(pdf_data)
