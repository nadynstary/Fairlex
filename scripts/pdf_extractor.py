from pypdf import PdfReader 
def extract_text_pdf(file_path:str) -> str:
    pdf_reader= PdfReader(file_path)
    text=""
    for page in pdf_reader.pages:
        text+=page.extract_text()+ "\n"
    return text
if __name__=="__main__":
    extracted_text=extract_text_pdf(r"C:\Users\nadeen\Downloads\terms-and-conditions-template-03.pdf")
    print(extracted_text[:300])