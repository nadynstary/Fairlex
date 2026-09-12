from pypdf import PdfReader 
import streamlit as st
import tempfile 


def extract_text_pdf(file_path:str) -> str:
    pdf_reader= PdfReader(file_path)
    text=""
    for page in pdf_reader.pages:
        text+=page.extract_text()+ "\n"
    return text

"""the file path"""
uploaded_file= st.file_uploader("Uplaod your PDF document here", type=["pdf"])
if uploaded_file is not None:
    with tempfile.NamedTempraryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path=tmp_file.name
    extracted_text= extract_text_pdf(tmp_file_path)
    ##the streamlit text area to display the extracted text
    st.text_area("Extracted text preview", value=extracted_text, height=300)



if __name__=="__main__":
    extracted_text=extract_text_pdf(r"C:\Users\nadeen\Downloads\terms-and-conditions-template-03.pdf")
    print(extracted_text[:300])