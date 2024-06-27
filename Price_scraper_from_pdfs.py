import streamlit as st

uploaded_file = st.file_uploader("Choose your .pdf file", type="pdf")

st.write(uploaded_file)
