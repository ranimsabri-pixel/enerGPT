# build_database.py — Indexation COMPLETE des 8117 chunks (étape 3)

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from chromadb.utils import embedding_functions
import os

print("=== CONSTRUCTION DE LA BASE COMPLETE ===")

# 1. Lecture + découpage (identique à l'étape 2)
pdf_files = [f for f in os.listdir("data") if f.endswith(".pdf")]
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

all_chunks = []
all_sources = []

for pdf_file in pdf_files:
    path = os.path.join("data", pdf_file)
    print(f"Lecture de : {pdf_file}")
    reader = PdfReader(path)
    for page_number, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            for chunk in splitter.split_text(text):
                all_chunks.append(chunk)
                all_sources.append(f"{pdf_file} (page {page_number + 1})")

print(f"\nTotal de chunks : {len(all_chunks)}")

# 2. Modèle d'embeddings local
print("Chargement du modèle d'embeddings...")
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# 3. Base PERSISTANTE (sauvegardée dans le dossier chroma_db/)
client = chromadb.PersistentClient(path="chroma_db")

# On supprime une éventuelle ancienne version pour repartir propre
try:
    client.delete_collection("energpt")
    print("Ancienne base supprimée.")
except Exception:
    pass

collection = client.create_collection(
    name="energpt",
    embedding_function=embedding_fn
)

# 4. Ajout par lots (batches) pour gérer les 8117 chunks
print("Création des embeddings (cela prend quelques minutes)...")
batch_size = 500

for i in range(0, len(all_chunks), batch_size):
    fin = i + batch_size
    collection.add(
        documents=all_chunks[i:fin],
        metadatas=[{"source": s} for s in all_sources[i:fin]],
        ids=[f"chunk_{j}" for j in range(i, min(fin, len(all_chunks)))]
    )
    print(f"  {min(fin, len(all_chunks))} / {len(all_chunks)} chunks traités")

print("\n=== BASE COMPLETE CONSTRUITE ET SAUVEGARDEE ===")
print(f"Nombre total d'éléments dans la base : {collection.count()}")