import json 
import numpy as np
import chromadb
from pathlib import Path

#r for raw
ROOT = Path(r"C:\Users\nadeen\OneDrive\Desktop\RAG_resources")

#dictionary brackets: the files and the jurisdictions they belong to. They have to be the same order i made them in. 
FILES = { "chunks_GDPR.json": "EU",
    "chunks_BH_PDPL.json": "BH",
    "chunks_SA_PDPL.json": "SA",
    "chunks_UNFAIR_TERMS.json": "EU",}

chunks = []

for f, jur in FILES.items():
    data = json.loads((ROOT / f).read_text(encoding="utf-8"))
    for c in data:
        c["jurisdiction"] = jur
    chunks += data

vectors = np.load(ROOT / "embeddings.npy")
print(len(chunks), "chunks,", vectors.shape, "vectors")
print (len(chunks)==len(vectors), "if false, chunks and vectors don't match, re-embed")

def make_id(c):
    base = f'{c["source"]}-{c["article"]}'
    if "item" in c:
        base += f'-{c["item"]}-{c.get("seq", 0)}'
    return f'{base}-{c["part"]}'

ids = [make_id(c) for c in chunks]
assert len(set(ids))==len(ids), "duplicate ids"

#only string allowed in metadata, so we convert the item to string if it exists.
metas = [{"source": c["source"], "jurisdiction": c["jurisdiction"],
          "article": c["article"], "item": str(c.get("item", None)) if c.get("item") is not None else None,
          "part": c["part"]} for c in chunks]

#bug fix: 
def clean(v):
    if isinstance(v, (str, int, float, bool)):
        return v
    return "" if v is None else str(v)

metas = [{k: clean(v) for k, v in m.items()} for m in metas]

client = chromadb.PersistentClient(path=str(ROOT / "chroma_db"))


#deletes trail runs and raises a pass for the first run
try:
    client.delete_collection("legal")
except Exception:
    pass


col = client.create_collection("legal", metadata={"hnsw:space":"cosine"})



col.add(ids=ids,
        embeddings=vectors.tolist(),
        metadatas=metas,
        documents=[c["text"] for c in chunks])

print("stored", col.count())
