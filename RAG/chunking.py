import re, json 
from pathlib import Path
import pymupdf #instaed of pypdf

ROOT = Path(r"C:\Users\nadeen\OneDrive\Desktop\RAG_resources")

""" reading the pdf files """
def read_file(path: Path) -> str:
    if path.suffix == ".pdf":
        with pymupdf.open(path) as doc:
            return "\n".join(page.get_text() for page in doc)
    return path.read_text(encoding="utf-8")
ARTICLE_RE = re.compile(r"^[ \t]*Article[ \t]*\(?(\d+)\)?(?:[ \t]+[A-Z][^\n]*)?[ \t]*$", re.MULTILINE)

def split_long(text, max_chars=3000, overlap=300):
    if len (text) <= max_chars:
        return [text]
    parts, start = [], 0
    while start < len(text):
        parts.append(text[start:start+max_chars])
        start += max_chars - overlap
    return parts

def chunk_law(text, law, jurisdiction):
    matches = list(ARTICLE_RE.finditer(text))
    chunks=[]
    for i , m in enumerate (matches):
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        body = text[m.start():end].strip()
        for j,piece in enumerate(split_long(body)):
            chunks.append({'source': law,"jurisdiction": jurisdiction, 'article': m.group(1),'part': j, 'text': piece})
    return chunks



ANNEX_RE = re.compile(r"^[ \t]*ANNEX\b[^\n]*$", re.MULTILINE)
ITEM_RE  = re.compile(r"^[ \t]*\(([a-z])\)[ \t]+", re.MULTILINE)

def split_annex(text):
    m = ANNEX_RE.search(text)
    if not m:
        return text, ""
    nxt = ARTICLE_RE.search(text, m.end())          # next article heading after the annex
    end = nxt.start() if nxt else len(text)
    annex = text[m.start():end]
    rest = text[:m.start()] + "\n" + text[end:]
    return rest, annex

def chunk_annex(annex, source, jurisdiction):
    matches = list(ITEM_RE.finditer(annex))
    if not matches:
        return [{"source": source, "jurisdiction": jurisdiction,
                 "article": "Annex", "item": "all",
                 "part": 0, "text": annex.strip()}]
    intro = annex[:matches[0].start()].strip()
    chunks = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(annex)
        body = annex[m.start():end].strip()
        chunks.append({"source": source, "jurisdiction": jurisdiction,
                       "article": "Annex", "item": f"({m.group(1)})", "seq": i,
                       "part": 0, "text": intro + "\n" + body})
    return chunks





""" -------------------- GDPR chunking and saving to json file --------------------"""
if __name__=="__main__":
    text = read_file(ROOT/"EU_GDPR.pdf")
    print("total length:", len(text))

    text = text.replace("\xa0", " ").replace("\u00ad", "")


    marker = re.search(r"HAVE\s+ADOPTED\s+THIS\s+REGULATION:", text, re.IGNORECASE)
    if marker:
        print("marker found at", marker.start())
        text = text[marker.start():]
    else:
        print("marker NOT found, using full text")
    print("length after cut:", len(text))

    print(repr(text[:500]))
    print("times 'Article' appears:", text.count("Article"))
    for n in (1, 2, 25, 90):
        i = text.find(f"Article {n}")
        print(n, i, repr(text[max(0, i-30):i+80]) if i != -1 else "not found")

    chunks = chunk_law(text, "GDPR", "EU")
    found = {int(c["article"]) for c in chunks}
    print(len(found), "articles found")
    print("missing:", [n for n in range(1, 100) if n not in found])

    out_path = ROOT / "chunks_GDPR.json"
    out_path.write_text(
        json.dumps(chunks, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Saved to:", out_path.resolve())



    """ -------------------- BH PDPL chunking and saving to json file --------------------"""
if __name__=="__main__":
    text = read_file(ROOT/"BH_PDPL.pdf")

    text = text.replace("\xa0", " ").replace("\u00ad", "")


    marker = re.search(r"HAVE\s+ADOPTED\s+THIS\s+REGULATION:", text, re.IGNORECASE)
    if marker:
        print("marker found at", marker.start())
        text = text[marker.start():]
    else:
        print("marker NOT found, using full text")
    print("length after cut:", len(text))

   

    chunks = chunk_law(text, "BH_PDPL", "Bahrain")
    found = {int(c["article"]) for c in chunks}
    print(len(found), "articles found")
    print("missing:", [n for n in range(1, 61) if n not in found])

########### sees if there are any articles that have more than one part, and prints them out
    from collections import Counter
    c = Counter(ch["article"] for ch in chunks if ch["part"] == 0)
    print([a for a, n in c.items() if n > 1]) 





    out_path = ROOT / "chunks_BH_PDPL.json"
    out_path.write_text(
        json.dumps(chunks, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Saved to:", out_path.resolve())

"""------------------------------------------------------------------------------------------------
------------------------------- Saudi PDPL chunking and saving to json file --------------------
------------------------------------------------------------------------------------------------"""

if __name__=="__main__":
    text = read_file(ROOT/"SA_PDPL.pdf")
    print("total length:", len(text))

    text = text.replace("\xa0", " ").replace("\u00ad", "")


#no need to cut the text or set a marker for the saudi PDPL 

    print(repr(text[:500]))
    print("times 'Article' appears:", text.count("Article"))

    chunks = chunk_law(text, "SA_PDPL", "Saudi Arabia")
    found = {int(c["article"]) for c in chunks}
    print(len(found), "articles found")
    print("missing:", [n for n in range(1, 44) if n not in found])

########### sees if there are any articles that have more than one part, and prints them out
    from collections import Counter
    c = Counter(ch["article"] for ch in chunks if ch["part"] == 0)
    print([a for a, n in c.items() if n > 1]) 



    out_path = ROOT / "chunks_SA_PDPL.json"
    out_path.write_text(
        json.dumps(chunks, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Saved to:", out_path.resolve())



    """-----------------------------------------------------------------------------------------------------------
    -------------------------------------- UNFAIR CLAUSES DOCUMENT CHUNKING --------------------------------------
    -----------------------------------------------------------------------------------------------------------------"""


if __name__=="__main__":
    text = read_file(ROOT/"UNFAIR_TERMS.pdf")
    print("total length:", len(text))

    text = text.replace("\xa0", " ").replace("\u00ad", "")


#no need to cut the text or set a marker for the saudi PDPL 

    print(repr(text[:500]))
    print("times 'Article' appears:", text.count("Article"))

    chunks = chunk_law(text, "UNFAIR_TERMS", "EU")
    found = {int(c["article"]) for c in chunks}
    print(len(found), "articles found")
    print("missing:", [n for n in range(1, 12) if n not in found])

########### sees if there are any articles that have more than one part, and prints them out
    from collections import Counter
    c = Counter(ch["article"] for ch in chunks if ch["part"] == 0)
    print([a for a, n in c.items() if n > 1]) 

    #ANNEX
    rest, annex = split_annex(text)
    print("annex length:", len(annex)); print(repr(annex[:300]))

    chunks  = chunk_law(rest, "EU Unfair Terms Directive", "EU")
    chunks += chunk_annex(annex, "EU Unfair Terms Directive", "EU")

    #JSON OUTPUT
    out_path = ROOT / "chunks_UNFAIR_TERMS.json"
    out_path.write_text(
        json.dumps(chunks, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Saved to:", out_path.resolve())
