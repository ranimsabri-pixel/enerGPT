langchain
langchain-community --(C'est la boîte à outils qui relie toutes les pièces entre elles : lire les documents, les découper, parler à la base vectorielle, parler au LLM.)
pypdf-- le lecteur de PDF
Les rapports sur les énergies renouvelables (IEA, IRENA) sont en PDF. pypdf ouvre ces fichiers et en extrait le texte brut pour que ton programme puisse le traiter.
chromadb-- la base vectorielle
C'est l'endroit où on stocke les embeddings (le texte transformé en nombres) et où on les retrouve très vite par le sens. C'est le « moteur de recherche » de ton RAG. Je l'ai choisie parce qu'elle est gratuite, locale (rien à payer, rien dans le cloud) et très simple pour débuter.
sentence-transformers--le fabricant d'embeddings (gratuit)
C'est lui qui transforme chaque morceau de texte en nombres. Il utilise des modèles gratuits de Hugging Face qui tournent sur ta machine — donc zéro coût, contrairement aux embeddings payants d'OpenAI. C'est la pièce qui rend ton projet « 100 % gratuit » côté embeddings.
streamlit-- l'interface visuelle
C'est lui qui transforme ton code Python en une vraie page web avec une zone de chat, sans que tu aies à apprendre le développement web (HTML, JavaScript). Quelques lignes de Python suffisent. C'est aussi ce qui te permettra de déployer l'app en ligne gratuitement. 

GroqCloud

modèle embedding : all-MiniLM-L6-v2 (local)

PS C:\Users\ranim\OneDrive\Bureau\enerGPT> py -3.11 -m venv venv
PS C:\Users\ranim\OneDrive\Bureau\enerGPT> .\venv\Scripts\activate


streamlit run app.py