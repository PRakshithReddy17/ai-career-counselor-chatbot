import json
from sentence_transformers import SentenceTransformer
import faiss

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load data
with open("data/careers.json") as f:
    careers = json.load(f)

texts = [c["career"] + " " + c["description"] for c in careers]

# Create embeddings
embeddings = model.encode(texts)

# Store in FAISS
index = faiss.IndexFlatL2(len(embeddings[0]))
index.add(embeddings)

def search(query):
    q_embedding = model.encode([query])
    _, I = index.search(q_embedding, k=1)
    return careers[I[0][0]]