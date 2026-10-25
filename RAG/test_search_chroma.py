import chromadb
from pathlib import Path 
from sentence_transformers import SentenceTransformer  

ROOT =  Path (r"C:\Users\nadeen\OneDrive\Desktop\RAG_resources")

model = SentenceTransformer("BAAI/bge-m3")
model.max_seq_length = 1024 

client = chromadb.PersistentClient(path=str(ROOT/"chroma_db"))
col = client.get_collection("legal")

#bug fix: adding kwargs, a dictionary argument. unpack where 
def search(query, n=5, jurisdiction=None):
    qv = model.encode([query], normalize_embeddings=True).tolist()
    kwargs = {"query_embeddings": qv, "n_results": n}
    if jurisdiction:
        kwargs["where"] = {"jurisdiction": jurisdiction}
    res = col.query(**kwargs)

    print("\nQ:", query, "| filter:", jurisdiction)
    for m, d, doc in zip(res["metadatas"][0], res["distances"][0], res["documents"][0]):
        label = f'{m["source"]} Art.{m["article"]} {m["item"]}'.strip()
        print(f"  {d:.3f}  {label}  |  {' '.join(doc.split())[-150:]!r}")


search("The comapny may share my data with advertising partners")
search("تسمح الشركة مشاركة بياناتي الشخصية مع المعلنين")
search("We can change these terms at any time without notice")
search("You waive your right to take legal action against us")
