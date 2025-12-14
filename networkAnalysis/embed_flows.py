import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb

INPUT = "flow_texts.csv"
DB_DIR = "flow_db"

def run():
    # Load text data
    df = pd.read_csv(INPUT)
    
    # Load embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # Create Chroma client
    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_or_create_collection(
        name="flows",
        metadata={"hnsw:space": "cosine"}
    )
    
    # Generate embeddings and insert into DB
    texts = df["text"].tolist()
    ids = [f"flow_{i}" for i in range(len(df))]
    embeddings = model.encode(texts).tolist()
    
    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings
    )
    
    print("✔ Embeddings stored in ChromaDB!")

if __name__ == "__main__":
    run()
