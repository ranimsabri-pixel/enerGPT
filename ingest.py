from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

print("=== DEMARRAGE ===")

if not os.path.exists("data"):
    print("Dossier data introuvable")
    exit()

pdf_files = [f for f in os.listdir("data") if f.endswith(".pdf")]
print("PDF trouvés :", len(pdf_files))

if len(pdf_files) == 0:
    print("Aucun PDF trouvé")
    exit()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

# On garde une liste de chunks AVEC leur source
all_chunks = []      # le texte de chaque morceau
all_sources = []     # d'où vient chaque morceau

for pdf_file in pdf_files:
    path = os.path.join("data", pdf_file)
    print(f"Lecture de : {pdf_file}")
    reader = PdfReader(path)

    # On lit ce PDF page par page en notant le numéro de page
    for page_number, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            # On découpe le texte de CETTE page
            page_chunks = splitter.split_text(text)
            for chunk in page_chunks:
                all_chunks.append(chunk)
                all_sources.append(f"{pdf_file} (page {page_number + 1})")

print(f"\nNombre total de chunks : {len(all_chunks)}")
print("\n=== PREMIER CHUNK ===")
print(all_chunks[0][:500])
print("\n=== SA SOURCE ===")
print(all_sources[0])