import streamlit as st
import PyPDF2

# Function to extract text from the uploaded PDF file
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfFileReader(uploaded_file)
    text = ""
    for page_num in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page_num)
        text += page.extract_text()
    return text

# Streamlit app
st.title("PDF Text Extractor")

uploaded_file = st.file_uploader("Choose your .pdf file", type="pdf")
if uploaded_file is not None:
    text = extract_text_from_pdf(uploaded_file)
    st.text_area("Extracted Text", text, height=300)
