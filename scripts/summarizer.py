from google import genai
from dotenv import load_dotenv
import os
load_dotenv()
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def summarizer(text:str) -> str:
    prompt=f"""you are fairlex, a legal document summarizer for non-technical users
Summarize the following document in plain, simple language.PermissionError
Highlight the key risks (data sharing, unusual clauses, rights being waived) that follow agreeing to this legal document, and give a hypothesis related to that risk for better understanding ).
Document :
{text}
"""
    response = client.models.generate_content(
        model= "gemini-3.6-flash"
        contents=prompt
    )
    return response.text
if __name__=="__main__":
    user_text= input("Paste the legal document text here: ")
    print(summarizer(user_text))


#========================= Feature 2: pdf2text=====================
from pdf_extractor import extract_text_pdf
if __name__=="__main__":
    extracted_text= extract_text_pdf(r"C:\Users\nadeen\Downloads\terms-and-conditions-template-03.pdf")
    summary= summarizer(extracted_text)
    print(summary)
