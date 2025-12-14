LLM Network Traffic Analysis System

AI-powered network flow analysis using PCAP → Flows → Embeddings → Semantic Search → Local LLM (Ollama) → Streamlit UI.

🚀 Overview

This project transforms raw PCAP network captures into meaningful cybersecurity insights using:

PyShark for packet extraction

Custom flow generator

Sentence Transformers for embeddings

ChromaDB for semantic search

Ollama (Llama 3.2) for local LLM analysis

Streamlit for an interactive UI

The system can detect suspicious flows, classify traffic, answer security questions, and let you explore network behavior using natural language.

Architecture
PCAP → PyShark → Packets → Flow Aggregation → Flow Descriptions
        ↓                               ↓
   Embeddings (Sentence Transformers) → ChromaDB (Vector DB)
        ↓
   Semantic Search
        ↓
Local LLM via Ollama (Llama 3.2)
        ↓
Streamlit UI → Security Insights
Features
✔ PCAP Parsing

Extracts packets using PyShark.

✔ Flow Aggregation

Groups packets into TCP/UDP flows.

✔ Flow-to-Text Pipeline

Converts flows into human-readable descriptions.

✔ Embeddings + Vector DB

Stores flows using Sentence Transformers + ChromaDB.

✔ Semantic Search

Find matching flows based on natural-language queries.

✔ Local LLM Threat Analysis

Uses Ollama Llama3.2 for on-device cybersecurity reasoning.

✔ Streamlit User Interface

Clean dashboard for search + AI analysis.

🛠️ Installation
1. Clone the repository
git clone https://github.com/YOUR_USERNAME/llm-network-analysis.git
cd llm-network-analysis

2. Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

3. Install dependencies
pip install -r requirements.txt

4. Install Ollama + LLM model

Download Ollama (Windows/macOS/Linux):
https://ollama.com/download

Then:

ollama pull llama3.2

▶️ Running the App

Run the Streamlit dashboard:

python -m streamlit run app.py

📸 Screenshots

Add screenshots inside screenshots/ and reference them here.

📚 Future Enhancements

PCAP upload from UI

Threat scoring (Low / Medium / High / Critical)

MITRE ATT&CK classification

Flow visualizations (charts, tables)

Anomaly detection rules

🧑‍💻 Author

Yashaswini I V — CSE Student