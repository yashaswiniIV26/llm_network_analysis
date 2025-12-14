import chromadb

DB_DIR = "flow_db"

def run():
    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_collection("flows")

    # user query
    query = "find HTTP traffic or suspicious communication"

    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    print("\n=== SEMANTIC SEARCH RESULTS ===")
    for doc in results["documents"][0]:
        print(doc)
        print("---------------------------")

if __name__ == "__main__":
    run()
