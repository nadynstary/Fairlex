import pymupdf
from docx import Document 

def read_file(source) -> str:
    is_path = isinstance(source, str)
    name=(source if is_path else source.name).lower()

    if name.endswith(".pdf"):
        if is_path:
            doc= pymupdf.open(source)
        else:
            doc= pymupdf.open(stream=source.read(),filetype="pdf")
        with doc:
            return "\n".join(page.get_text() for page in doc)
    if name.endswith(".pdf"):
        with pymupdf.open(stream=source.read(),filetype="pdf") as doc:
            return "\n".join(page.get_text() for page in doc)
    if name.endswith("docx"):
        return"\n".join(p.text for p in Document(source).paragraphs)
    if name.endswith(".txt"):
        return source.read().decode("utf-8", errors= "ignore")
    #if file type source none of the above
    raise ValueError("Unsupported file type")