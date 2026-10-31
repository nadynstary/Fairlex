import pymupdf
from docx import Document 

def read_file(source) -> str:
    name = uploaded.name.lower()
    if name.endswith(".pdf"):
        with pymupdf.open(stream=uploaded.read(),filetype="pdf") as doc:
            return "\n".join(page.get_text() for page in doc)
    if name.endswith("docx"):
        return"\n".join(p.text for p in Document(uploaded).paragraphs)
    if name.endswith(".txt"):
        return uploaded.read().decode("utf-8", errors= "ignore")
    #if file type uploaded none of the above
    raise ValueError("Unsupported file type")