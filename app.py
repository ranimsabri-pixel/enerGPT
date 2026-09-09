# app.py — Interface web de EnerGPT avec Streamlit (étape 5)

import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
from dotenv import load_dotenv
import os

# --- Configuration de la page ---
st.set_page_config(page_title="EnerGPT", page_icon="⚡", layout="centered")
st.title("⚡ EnerGPT")
st.caption("Assistant intelligent sur les énergies renouvelables — basé sur 23 rapports IEA & IRENA")

# --- Chargement de la clé API ---
load_dotenv()

# --- Chargement de la base (mis en cache pour ne le faire qu'une fois) ---
@st.cache_resource
def charger_base():
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    client_chroma = chromadb.PersistentClient(path="chroma_db")
    collection = client_chroma.get_collection(
        name="energpt",
        embedding_function=embedding_fn
    )
    return collection

collection = charger_base()
client_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- La fonction RAG (identique à chatbot.py) ---
def repondre(question):
    results = collection.query(query_texts=[question], n_results=4)
    passages = results["documents"][0]
    sources = [m["source"] for m in results["metadatas"][0]]

    contexte = ""
    for i, passage in enumerate(passages):
        contexte += f"[Extrait {i+1} - source : {sources[i]}]\n{passage}\n\n"

    prompt = f"""Tu es un assistant spécialisé dans les énergies renouvelables.
Réponds à la question en t'appuyant UNIQUEMENT sur les extraits fournis ci-dessous.
Si l'information n'est pas dans les extraits, dis-le honnêtement.
Cite les sources que tu utilises.

EXTRAITS :
{contexte}

QUESTION : {question}

REPONSE :"""

    completion = client_groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return completion.choices[0].message.content, sources

# --- Gestion de l'historique de conversation ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher l'historique existant
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Zone de saisie ---
if question := st.chat_input("Pose ta question sur les énergies renouvelables..."):
    # Afficher la question de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Générer et afficher la réponse
    with st.chat_message("assistant"):
        with st.spinner("Recherche dans les documents..."):
            reponse, sources = repondre(question)
        st.markdown(reponse)
    st.session_state.messages.append({"role": "assistant", "content": reponse})