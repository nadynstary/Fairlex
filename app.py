import streamlit as st
from scripts.summarizer import summarizer
from scripts.categorization import CATEGORIES_PROMPTS
from scripts.pdf_extractor import read_file
from scripts.url_extractor import extract_text_url

st.set_page_config(page_title="FairLex", page_icon="⚖️")
st.title("FairLex")

category = st.selectbox("What kind of document is this?", list(CATEGORIES_PROMPTS.keys()))
tab_pdf, tab_text, tab_url = st.tabs(["Upload file", "Paste text", "Paste URL"])

text = None
with tab_pdf:
    f = st.file_uploader("Upload your document", type=["pdf", "docx", "txt"])
    if f:
        text = read_file(f)
with tab_text:
    pasted = st.text_area("Paste the text here", height=200)
    if pasted:
        text = pasted
with tab_url:
    url = st.text_input("Link to the Terms & Conditions page")
    if url and st.button("Fetch page"):
        try:
            text = extract_text_url(url)
        except Exception as e:
            st.error(str(e))

if text and st.button("Summarize"):
    with st.spinner("Reading the document..."):
        st.write(summarizer(text, category))