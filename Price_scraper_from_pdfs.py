import streamlit as st
import pdfplumber
import pandas as pd

# File uploader for multiple files
uploaded_files = st.file_uploader("Choose your .pdf files", type="pdf", accept_multiple_files=True)

# Check if files have been uploaded
if uploaded_files:
    all_text = ""
    for uploaded_file in uploaded_files:
        with pdfplumber.open(uploaded_file) as pdf_file:
            pdf_text = ""
            for page in pdf_file.pages:
                pdf_text += page.extract_text()
            all_text += pdf_text + "\n\n"  # Adding new lines for separation between different PDFs

    st.text_area("Extracted Text", all_text, height=500)
