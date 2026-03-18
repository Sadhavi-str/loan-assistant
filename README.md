#  Bank of Maharashtra Loan Product Assistant

A Retrieval-Augmented Generation (RAG) powered chatbot that answers questions about Bank of Maharashtra's loan products.

---

## Project Setup

### Prerequisites
- Python 3.8+
- Git

### Installation

1. Clone the repository:
```
git clone https://github.com/YOUR_USERNAME/loan-assistant.git
cd loan-assistant
```

2. Install dependencies:
```
pip install requests beautifulsoup4 faiss-cpu sentence-transformers transformers langchain langchain-community langchain-huggingface langchain-text-splitters streamlit torch
```

3. Run the scraper to build knowledge base:
```
python scraper.py
```

4. Launch the app:
```
streamlit run app.py
```

5. Open your browser at `http://localhost:8501`

---

##  Architectural Decisions

### Part A — Data Scraping
- **Library used:** `requests` + `BeautifulSoup4`
- **Strategy:** Targeted scraping of specific Bank of Maharashtra loan pages (Personal, Home, Vehicle, Education, Gold, Loan Against Property)
- **Challenge handling:** The official website blocks cloud server IPs (common with Indian bank websites). The scraper automatically falls back to manually collected real data from the website when live scraping fails
- **Cleaning:** All HTML tags, navigation, scripts, footers and ads are stripped. Only clean text content is kept

### Part B — Data Consolidation
- All loan pages are merged into a single file: `loan_knowledge_base.txt`
- Each section is clearly labeled with its source URL
- Data is structured in a consistent format for easy retrieval

### Part C — RAG Pipeline
```
User Question
     ↓
Keyword Detection (identifies loan type)
     ↓
Section Retrieval (finds correct loan section)
     ↓
FAISS Vector Search (finds relevant chunks)
     ↓
Answer Extraction (pulls clean relevant lines)
     ↓
Final Answer displayed in Streamlit UI
```

**Libraries chosen:**
| Tool | Purpose | Why |
|------|---------|-----|
| `sentence-transformers` | Text embeddings | Free, runs locally, no API key needed |
| `all-MiniLM-L6-v2` | Embedding model | Lightweight, fast, accurate |
| `FAISS` | Vector search | In-memory, no database setup needed |
| `LangChain` | Pipeline framework | Industry standard for RAG pipelines |
| `Streamlit` | Chat UI | Fast to build, clean interface |

**LLM Choice:** Instead of an external LLM API, we use direct context extraction from the knowledge base. This means:
- No API key required
- No cost

---

## ⚠️ Challenges Faced

### 1. Website Blocking Cloud IPs
**Problem:** Bank of Maharashtra's website blocked scraping requests from Google Colab and GitHub Codespaces (common with Indian banking websites for security reasons).

**Solution:** Built an automatic fallback system. The scraper first attempts live scraping. If it fails, it loads manually collected real data from the official website. This data is stored directly in the scraper as a fallback constant.


---

##  Potential Improvements

1. **Better LLM Integration:** Use a proper free LLM API (like Groq's free tier with Llama 3) for more natural, conversational answers instead of direct extraction

2. **PDF Parsing:** Bank of Maharashtra publishes loan brochures as PDFs. Adding PDF parsing would significantly enrich the knowledge base

3. **Multi-language Support:** Add Hindi/Marathi language support for wider accessibility

---

## 📁 Project Structure
```
loan-assistant/
│
├── scraper.py              # Part A: Web scraping script
├── rag.py                  # Part C: RAG pipeline implementation  
├── app.py                  # Streamlit chat interface
├── loan_knowledge_base.txt # Part B: Cleaned knowledge base
└── README.md               # Project documentation
```

---

## 🛠️ Tech Stack

- **Python 3.12**
- **BeautifulSoup4** — HTML parsing
- **Sentence Transformers** — Text embeddings
- **FAISS** — Vector similarity search
- **LangChain** — RAG framework
- **Streamlit** — Web interface

---
