import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

def run(text_file="flow_texts.csv", db_path="flow_db"):
    """
    Embed natural-language flow descriptions and store them in ChromaDB.
    """

    print("[INFO] Loading model...")
    model = SentenceTransformer("all-mpnet-base-v2")

    print("[INFO] Reading text file...")
    df = pd.read_csv(text_file)
    texts = df["text"].tolist()

    print("[INFO] Connecting to ChromaDB...")
    db = chromadb.PersistentClient(path=db_path)

    try:
        col = db.get_collection("flows")
        print("[INFO] Using existing collection.")
    except:
        col = db.create_collection("flows")
        print("[INFO] Created new collection.")

    print("[INFO] Generating embeddings...")
    embeddings = model.encode(texts).tolist()

    print("[INFO] Storing embeddings...")
    col.add(
        documents=texts,
        embeddings=embeddings,
        ids=[f"id_{i}" for i in range(len(texts))]
    )

    print("[OK] Embeddings stored successfully!")


if __name__ == "__main__":
    run()
