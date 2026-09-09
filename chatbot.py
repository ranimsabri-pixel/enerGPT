# chatbot.py — Le RAG complet : recherche + réponse par Groq (étape 4)

import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
from dotenv import load_dotenv
import os

# 1. Charger la clé API depuis le fichier .env
load_dotenv()
client_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 2. Recharger la base ChromaDB déjà construite (pas de recalcul !)
print("Chargement de la base...")
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
client_chroma = chromadb.PersistentClient(path="chroma_db")
collection = client_chroma.get_collection(
    name="energpt",
    embedding_function=embedding_fn
)
print(f"Base chargée : {collection.count()} chunks disponibles.\n")

# 3. La fonction qui répond à une question
def repondre(question):
    # a) Recherche des passages pertinents
    results = collection.query(query_texts=[question], n_results=4)
    passages = results["documents"][0]
    sources = [m["source"] for m in results["metadatas"][0]]

    # b) On assemble le contexte (les extraits trouvés)
    contexte = ""
    for i, passage in enumerate(passages):
        contexte += f"[Extrait {i+1} - source : {sources[i]}]\n{passage}\n\n"

    # c) On construit le prompt pour le LLM
    prompt = f"""Tu es un assistant spécialisé dans les énergies renouvelables.
Réponds à la question en t'appuyant UNIQUEMENT sur les extraits fournis ci-dessous.
Si l'information n'est pas dans les extraits, dis-le honnêtement.
Cite les sources que tu utilises.

EXTRAITS :
{contexte}

QUESTION : {question}

REPONSE :"""

    # d) On envoie à Groq
    completion = client_groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return completion.choices[0].message.content

# 4. Boucle de discussion dans le terminal
print("=== EnerGPT prêt ! Pose tes questions (tape 'quit' pour sortir) ===\n")
while True:
    question = input("Ta question : ")
    if question.lower() in ["quit", "exit", "q"]:
        break
    reponse = repondre(question)
    print("\n--- REPONSE ---")
    print(reponse)
    print("\n" + "=" * 50 + "\n")