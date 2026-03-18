import streamlit as st
from rag import build_rag
import os
import subprocess

st.set_page_config(page_title="BOM Loan Assistant", page_icon="🏦", layout="centered")
st.title("🏦 Bank of Maharashtra")
st.subheader("Loan Product Assistant")
st.markdown("*Powered by RAG Pipeline — 100% Free & Local*")
st.divider()

@st.cache_resource
def load_pipeline():
    if not os.path.exists("loan_knowledge_base.txt"):
        subprocess.run(["python", "scraper.py"])
    return build_rag()

with st.spinner("⏳ Loading AI pipeline... please wait"):
    qa_chain = load_pipeline()

st.success("✅ Assistant ready!")

st.markdown("### 💡 Try these questions:")
cols = st.columns(2)
sample_qs = [
    "What are home loan interest rates?",
    "Personal loan tenure for salary account holders?",
    "Tell me about Maha Super Flexi Housing Loan",
    "Concessions for women on home loans?"
]
for i, q in enumerate(sample_qs):
    with cols[i % 2]:
        if st.button(q, use_container_width=True):
            st.session_state["prefill"] = q

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask about any Bank of Maharashtra loan product...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = qa_chain(prompt)
            answer = result["result"]
        st.markdown(answer)
        st.caption("📎 Based on Bank of Maharashtra official data")
    st.session_state.messages.append({"role": "assistant", "content": answer})