import streamlit as st
import pdfplumber
import pandas as pd

uploaded_file = st.file_uploader("Choose your .pdf file", type="pdf", accept_multiple_files=True)

with pdfplumber.open(uploaded_file) as pdf_file:
  pdf_text = ""
  for page in pdf_file.pages:
      pdf_text += page.extract_text()


st.write(pdf_text)
