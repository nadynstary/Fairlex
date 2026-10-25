import json 
from pathlib import Path
import numpy as np
import torch
from sentence_transformers import SentenceTransformer


ROOT = Path(r"C:\Users\nadeen\OneDrive\Desktop\RAG_resources")
FILES = ["chunks_GDPR.json", "chunks_BH_PDPL.json",
          "chunks_SA_PDPL.json","chunks_UNFAIR_TERMS.json"]
chunks = []
for f in FILES:
    data = json.loads((ROOT / f).read_text(encoding="utf-8"))
    print(f, len(data), "chunks")
    chunks += data
print("total chunks", len(chunks))


# assign an id for each chunk

def make_id(c):
    base = f'{c["source"]}-{c["article"]}'
    if "item" in c:
        base += f'-{c["item"]}-{c.get("seq", 0)}'
    return f'{base}-{c["part"]}'



# the text that will be embedded (header + chunk)
def header(c):
    h = f'{c["source"]}, Article {c["article"]}'
    if "item" in c:
        h += f' item {c["item"]}'
    return h

ids  = [make_id(c) for c in chunks]
docs = [header(c) + ": " + c["text"] for c in chunks]

assert len(set(ids)) == len(ids), "duplicate ids found"

print(ids[0])
print(docs[0][:300])
print("longest chunk (chars):", max(len(d) for d in docs))



torch.set_num_threads(4)

print("Loading model...")
model = SentenceTransformer("BAAI/bge-m3")
model.max_seq_length = 1024

print("Embedding", len(docs), "chunks...")
vectors = model.encode(docs, batch_size=4, normalize_embeddings=True,
                       show_progress_bar=True)

print("shape:", vectors.shape)          # expect (267, 1024)
np.save(ROOT / "embeddings.npy", vectors)
print("Saved embeddings.npy")