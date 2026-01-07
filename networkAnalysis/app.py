import streamlit as st
import os
import chromadb
from sentence_transformers import SentenceTransformer
import subprocess
import pandas as pd

# =========================
# Page Config
# =========================
st.set_page_config(page_title="AI Network Traffic Analysis", layout="wide")
st.title("🔐 AI Network Traffic Analysis (SOC-Style MVP)")

# =========================
# Constants
# =========================
PCAP_PATH = "uploaded.pcap"
PACKETS_CSV = "packets.csv"
FLOWS_CSV = "flows.csv"
FLOW_TEXTS_CSV = "flow_texts.csv"
DB_PATH = "flow_db"
EMBED_MODEL_NAME = "all-mpnet-base-v2"

# =========================
# Load Embedding Model
# =========================
@st.cache_resource
def load_model():
    return SentenceTransformer(EMBED_MODEL_NAME)

embed_model = load_model()

# =========================
# Semantic Search
# =========================
def semantic_search(query, top_k=5):
    db = chromadb.PersistentClient(path=DB_PATH)
    col = db.get_collection("flows")

    query_embedding = embed_model.encode([query]).tolist()
    results = col.query(query_embeddings=query_embedding, n_results=top_k)
    return results["documents"][0]

# =========================
# Risk Scoring
# =========================
def compute_risk_score(flows):
    score = 0
    reasons = []

    text = " ".join(flows).lower()

    if "unknown" in text:
        score += 2
        reasons.append("Unknown source or destination detected")

    if "udp" in text:
        score += 2
        reasons.append("UDP traffic observed")

    if "packet count 1" in text:
        score += 1
        reasons.append("Single-packet flow detected")

    if score == 0:
        reasons.append("No anomalous patterns detected")

    return min(score, 10), reasons

# =========================
# MITRE Mapping
# =========================
def map_to_mitre(flows):
    text = " ".join(flows).lower()
    techniques = []

    if "tcp" in text or "http" in text:
        techniques.append("T1071 – Application Layer Protocol")

    if "udp" in text:
        techniques.append("T1046 – Network Service Discovery")

    if "unknown" in text:
        techniques.append("T1049 – System Network Connections Discovery")

    if not techniques:
        techniques.append("No clear MITRE ATT&CK technique detected")

    return techniques

# =========================
# Mitigation Recommendations
# =========================
def recommend_actions(risk_score):
    if risk_score <= 2:
        return [
            "No immediate action required",
            "Continue monitoring network traffic",
            "Maintain current security controls"
        ]
    elif risk_score <= 5:
        return [
            "Investigate affected endpoints",
            "Review related logs and authentication attempts",
            "Increase monitoring sensitivity"
        ]
    else:
        return [
            "Temporarily block suspicious IPs",
            "Inspect endpoint for compromise",
            "Escalate to incident response team"
        ]

# =========================
# Sidebar Upload
# =========================
st.sidebar.header("📂 Upload PCAP")
uploaded_file = st.sidebar.file_uploader("Upload a PCAP file", type=["pcap"])

if uploaded_file:
    with open(PCAP_PATH, "wb") as f:
        f.write(uploaded_file.read())

    st.sidebar.success("PCAP uploaded")

    with st.spinner("Processing PCAP..."):
        import extract_pcap, create_flows, flow_to_text, embed_flows
        extract_pcap.run(PCAP_PATH, PACKETS_CSV)
        create_flows.run(PACKETS_CSV, FLOWS_CSV)
        flow_to_text.run(FLOWS_CSV, FLOW_TEXTS_CSV)
        embed_flows.run(FLOW_TEXTS_CSV, DB_PATH)

    st.sidebar.success("PCAP processed & indexed")

# =========================
# Main Query Panel
# =========================
st.subheader("🔎 Ask a Security Question")
query = st.text_input("Example: Is this network traffic suspicious?")

if st.button("Analyze"):
    if not os.path.exists(DB_PATH):
        st.error("Upload and process a PCAP first")
    else:
        flows = semantic_search(query)
        risk_score, reasons = compute_risk_score(flows)
        mitre = map_to_mitre(flows)
        actions = recommend_actions(risk_score)

        verdict = (
            "BENIGN" if risk_score <= 2
            else "NEEDS INVESTIGATION" if risk_score <= 5
            else "POTENTIALLY SUSPICIOUS"
        )

        confidence = "HIGH" if risk_score <= 2 else "MEDIUM" if risk_score <= 5 else "LOW"

        st.subheader("🧠 AI Security Analysis")
        st.markdown(f"""
**Verdict:** {verdict}  
**Risk Score:** {risk_score} / 10  
**Confidence:** {confidence}
""")

        st.markdown("**Key Reasons:**")
        for r in reasons:
            st.markdown(f"- {r}")

        st.markdown("**MITRE ATT&CK Mapping:**")
        for m in mitre:
            st.markdown(f"- {m}")

        st.markdown("**Recommended Actions:**")
        for a in actions:
            st.markdown(f"- {a}")

        st.markdown("---")

        prompt = f"""
You are a SOC analyst.

Relevant flows:
{chr(10).join(flows)}

Verdict: {verdict}
Risk Score: {risk_score}
Confidence: {confidence}

Explain the assessment and recommendations briefly.
"""

        response = subprocess.run(
            ["ollama", "run", "llama3.2", prompt],
            capture_output=True,
            text=True
        )

        st.markdown("### 🤖 AI Explanation")
        st.write(response.stdout)
