from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def build_rag():
    print("📄 Loading knowledge base...")
    with open("loan_knowledge_base.txt", "r") as f:
        text = f.read()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.create_documents([text])
    print(f"✅ {len(chunks)} chunks created")

    print("🧠 Loading embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("📦 Building FAISS index...")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    print("✅ RAG Pipeline ready!")

    def ask(question):
        q = question.lower()

        # Map question keywords to loan type
        if any(w in q for w in ["home loan", "housing", "house", "flexi", "maha super"]):
            loan_type = "home"
        elif any(w in q for w in ["personal loan", "personal"]):
            loan_type = "personal"
        elif any(w in q for w in ["vehicle", "car", "two wheeler", "bike"]):
            loan_type = "vehicle"
        elif any(w in q for w in ["education", "study", "student", "vidya"]):
            loan_type = "education"
        elif any(w in q for w in ["gold"]):
            loan_type = "gold"
        elif any(w in q for w in ["property", "lap"]):
            loan_type = "property"
        else:
            loan_type = None

        # Split knowledge base into sections
        with open("loan_knowledge_base.txt", "r") as f:
            full_text = f.read()

        sections = full_text.split("==============================")

        # Find the right section
        best_section = None
        if loan_type:
            for section in sections:
                s = section.lower()
                if loan_type == "home" and "home loan" in s:
                    best_section = section
                    break
                elif loan_type == "personal" and "personal loan" in s:
                    best_section = section
                    break
                elif loan_type == "vehicle" and "vehicle loan" in s:
                    best_section = section
                    break
                elif loan_type == "education" and "education loan" in s:
                    best_section = section
                    break
                elif loan_type == "gold" and "gold loan" in s:
                    best_section = section
                    break
                elif loan_type == "property" and "loan against property" in s:
                    best_section = section
                    break

        # If we found the right section, extract relevant lines
        if best_section:
            lines = best_section.strip().split("\n")
            clean_lines = []
            for line in lines:
                line = line.strip()
                if (len(line) > 15 and
                    "SOURCE" not in line and
                    "http" not in line and
                    "===" not in line):
                    clean_lines.append(line)

            # Further filter by question keywords
            q_words = [w for w in q.split() if len(w) > 3 and w not in ["what", "tell", "about", "loan", "bank", "maharashtra"]]

            # Try to find lines matching question keywords
            matched = []
            for line in clean_lines:
                if any(word in line.lower() for word in q_words):
                    matched.append(line)

            # If matches found show them, else show full section
            final_lines = matched if matched else clean_lines

            answer = "Here is the information from Bank of Maharashtra:\n\n"
            answer += "\n".join(f"• {l}" for l in final_lines[:8])
        else:
            # General question - use FAISS
            docs = vectorstore.similarity_search(question, k=2)
            context_lines = []
            for doc in docs:
                for line in doc.page_content.split("\n"):
                    line = line.strip()
                    if len(line) > 15 and "SOURCE" not in line and "http" not in line:
                        context_lines.append(line)
            if context_lines:
                answer = "Here is the information from Bank of Maharashtra:\n\n"
                answer += "\n".join(f"• {l}" for l in context_lines[:8])
            else:
                answer = "I don't have specific information about that. Please visit bankofmaharashtra.in for details."

        docs = vectorstore.similarity_search(question, k=2)
        return {"result": answer, "source_documents": docs}

    return ask