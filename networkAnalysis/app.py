import streamlit as st
import chromadb
import requests
import json
import pandas as pd

DB_DIR = "flow_db"
OLLAMA_URL = "http://localhost:11434/api/generate"

# --- Helpers ---

def semantic_search(query):
    db = chromadb.PersistentClient(path=DB_DIR)
    col = db.get_collection("flows")
    results = col.query(query_texts=[query], n_results=5)
    return results["documents"][0]

def ask_llm(context, question):
    prompt = f"""
You are a network security analyst.
Here is network flow data:

{context}

Question: {question}

Provide a detailed cybersecurity analysis.
"""

    data = {
        "model": "llama3.2",
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

# --- UI ---

st.title("🔍 LLM Network Traffic Analysis")
st.write("Search flows, view semantics, and get AI-driven threat analysis.")

query = st.text_input("Enter your search or question:")

if st.button("Analyze"):
    if query.strip() == "":
        st.warning("Please enter a question or search.")
    else:
        flows = semantic_search(query)
        st.subheader("🔎 Top Matching Flows")
        for f in flows:
            st.code(f)

        st.subheader("🤖 AI Security Analysis")
        context = "\n".join(flows)
        answer = ask_llm(context, query)
        st.write(answer)
