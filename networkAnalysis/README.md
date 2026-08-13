# 🔐 LLM Network Traffic Analysis

AI-powered network flow analysis that turns raw PCAP captures into SOC-style security insights, using a local LLM (Ollama) for natural-language explanations.

## Overview

This project builds a small pipeline that takes a raw packet capture and makes it queryable in plain English:

1. **Parse** packets out of a `.pcap` file with TShark
2. **Aggregate** packets into TCP/UDP flows
3. **Describe** each flow as a natural-language sentence
4. **Embed** those descriptions with Sentence Transformers and store them in ChromaDB
5. **Search** the flows semantically based on a user's question
6. **Score & explain** the result — a rule-based risk score, a MITRE ATT&CK mapping, and a written explanation from a local LLM (Llama 3.2 via Ollama)

Everything runs through a Streamlit dashboard: upload a PCAP, ask a question like *"Is this traffic suspicious?"*, and get a verdict, a risk score, relevant MITRE techniques, recommended actions, and an AI-generated explanation.

## Architecture

```
                 ┌──────────────┐
   .pcap file →  │   TShark     │  extract_pcap.py
                 └──────┬───────┘
                        ▼
                 packets.csv (per-packet rows)
                        ▼
                 ┌──────────────┐
                 │ Flow Builder │  create_flows.py
                 └──────┬───────┘  (groups by src/dst/port/proto)
                        ▼
                 flows.csv (per-flow aggregates)
                        ▼
                 ┌──────────────┐
                 │ Flow → Text  │  flow_to_text.py
                 └──────┬───────┘  (SOC-style sentences)
                        ▼
                 flow_texts.csv
                        ▼
                 ┌──────────────┐
                 │ Embeddings   │  embed_flows.py
                 │ (Sentence-   │  → ChromaDB ("flows" collection)
                 │ Transformers)│
                 └──────┬───────┘
                        ▼
                 ┌──────────────┐
                 │ Semantic     │  search_flows.py / app.py
                 │ Search       │
                 └──────┬───────┘
                        ▼
        ┌───────────────────────────────┐
        │ Rule-based analysis            │
        │  • risk score (0–10)           │
        │  • MITRE ATT&CK mapping        │
        │  • recommended actions         │
        └───────────────┬─────────────────┘
                        ▼
                 ┌──────────────┐
                 │ Local LLM     │  Ollama (llama3.2)
                 │ Explanation   │
                 └──────┬───────┘
                        ▼
                 Streamlit UI (app.py)
```

There's also a standalone RAG-style query script (`rag_query.py`) that skips the UI and lets you ask a free-form question against the vector DB directly from the terminal, streaming the answer from Ollama's `/api/generate` endpoint.

## Project structure

```
networkAnalysis/
├── app.py                   # Streamlit app — upload PCAP, run pipeline, ask questions
├── extract_pcap.py          # PCAP → packets.csv (via TShark)
├── create_flows.py          # packets.csv → flows.csv (flow aggregation)
├── flow_to_text.py          # flows.csv → flow_texts.csv (natural-language descriptions)
├── embed_flows.py           # flow_texts.csv → ChromaDB embeddings
├── search_flows.py          # standalone semantic search demo script
├── rag_query.py             # standalone CLI: question → semantic search → Ollama answer
├── requirements.txt         # Python dependencies
├── flows.csv, netflows.csv, flow_texts.csv   # sample/example pipeline outputs
├── sample_pcap_base64.txt   # sample capture, base64-encoded
├── screenshots/             # UI screenshots (ui_home.png, ui_analysis.png)
└── object.java              # unrelated scratch file (not part of the pipeline)
```

## How the risk scoring works

`app.py` uses simple keyword-based heuristics over the retrieved flow descriptions (not the LLM) to compute a score, then hands that score plus the flows to the LLM for an explanation:

| Signal in flow text | Points |
|---|---|
| `"unknown"` source/destination | +2 |
| `"udp"` traffic | +2 |
| single-packet flow (`"packet count 1"`) | +1 |

- **0–2** → `BENIGN` (High confidence)
- **3–5** → `NEEDS INVESTIGATION` (Medium confidence)
- **6+** → `POTENTIALLY SUSPICIOUS` (Low confidence)

MITRE ATT&CK techniques are mapped similarly by keyword: TCP/HTTP → T1071, UDP → T1046, unknown endpoints → T1049.

## Prerequisites

- Python 3.10+
- **[TShark](https://tshark.dev/)** installed and on your PATH (part of Wireshark) — required for `extract_pcap.py`
- **[Ollama](https://ollama.com/download)** installed, with the `llama3.2` model pulled

```bash
ollama pull llama3.2
```

## Installation

```bash
git clone https://github.com/yashaswiniIV26/llm_network_analysis.git
cd llm_network_analysis/networkAnalysis

python -m venv venv
# Windows
.\venv\Scripts\Activate.ps1
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

## Running the app

Make sure the Ollama service is running (`ollama serve`, or it's already running in the background after install), then:

```bash
python -m streamlit run app.py
```

1. Upload a `.pcap` file from the sidebar — this triggers the full pipeline (extract → flow → text → embed) automatically
2. Type a question in the main panel, e.g. *"Is this network traffic suspicious?"*
3. Click **Analyze** to get the verdict, risk score, MITRE mapping, recommended actions, and an AI-written explanation

## Standalone scripts

You can also run pieces of the pipeline independently against `sample.pcap` (or your own file) without the UI:

```bash
python extract_pcap.py       # → packets.csv
python create_flows.py       # → flows.csv
python flow_to_text.py       # → flow_texts.csv
python embed_flows.py        # → embeddings in ./flow_db
python search_flows.py       # sample semantic search over the DB
python rag_query.py          # interactive Q&A from the terminal
```

## Screenshots

| Home | Analysis |
|---|---|
| `screenshots/ui_home.png` | `screenshots/ui_analysis.png` |

## Future enhancements

- In-UI PCAP upload improvements / progress feedback for large captures
- Richer, model-based threat scoring instead of keyword heuristics
- Expanded MITRE ATT&CK technique coverage
- Flow visualizations (charts, timelines, traffic graphs)
- Configurable anomaly detection rules

## Author

Yashaswini I V — CSE Student
