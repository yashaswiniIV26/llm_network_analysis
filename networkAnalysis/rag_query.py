import os
import json   # ← REQUIRED
import chromadb
import requests

DB_DIR = "flow_db"
OLLAMA_URL = "http://localhost:11434/api/generate"

def semantic_search(query):
    db = chromadb.PersistentClient(path=DB_DIR)
    col = db.get_collection("flows")
    results = col.query(query_texts=[query], n_results=3)
    return "\n".join(results["documents"][0])

def ask_llm(context, question):
    prompt = f"""
You are a network security analyst.
Here is network flow data:

{context}

Question: {question}

Provide a detailed cybersecurity analysis.
"""

    data = {
        "model": "llama3.2",   # or "deepseek-r1:1.5b"
        "prompt": prompt,
        "stream": True
    }

    response = requests.post(OLLAMA_URL, json=data, stream=True)

    final_text = ""
    for line in response.iter_lines():
        if line:
            try:
                obj = json.loads(line.decode("utf-8"))
                final_text += obj.get("response", "")
            except:
                continue

    return final_text

def main():
    query = input("Enter your question: ")
    context = semantic_search(query)
    answer = ask_llm(context, query)
    print("\n=== AI ANALYSIS ===")
    print(answer)

if __name__ == "__main__":
    main()
