from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

# ── Load .env FIRST before anything else ──────────────────────────────────────
# Load .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print("API Key Loaded:", api_key[:10] + "..." if api_key else "NOT FOUND")

# Validate API Key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "❌ OPENAI_API_KEY is not set correctly.\n"
        "Create a .env file in the project root with:\n"
        "OPENAI_API_KEY=OPENAI_API_KEY\n"
    )


# ── Global chain reference ─────────────────────────────────────────────────────
retrieval_chain = None

# ── Lifespan: runs on startup and shutdown ─────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    global retrieval_chain

    print("🚀 Starting up — loading ChromaDB and building RAG chain...")

    embeddings = OpenAIEmbeddings()

    chroma_path = "./chroma_db"
    if not os.path.exists(chroma_path):
        raise RuntimeError(
            f"❌ ChromaDB folder '{chroma_path}' not found.\n"
            "Run your data ingestion script first to populate the vector store."
        )

    vector_store = Chroma(
        persist_directory=chroma_path,
        embedding_function=embeddings
    )

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(model="gpt-4o-mini")

    prompt = ChatPromptTemplate.from_template(
        "Answer the question about Farmer Schemes based ONLY on the provided context.\n\n"
        "Context: {context}\n\n"
        "Question: {input}"
    )

    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    print("✅ RAG chain ready — server is accepting requests.")

    yield  # ← Server runs here

    # Cleanup on shutdown
    retrieval_chain = None
    print("🛑 Server shutting down.")

# ── App instance ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="TNAU Farmer Schemes API",
    description="RAG-powered API for Tamil Nadu farmer scheme queries",
    version="1.0.0",
    lifespan=lifespan
)

# ── CORS — allows Streamlit frontend to call this API ─────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request model ──────────────────────────────────────────────────────────────
class Query(BaseModel):
    question: str

# ── Routes ─────────────────────────────────────────────────────────────────────
@app.get("/")
async def root():
    return {
        "app": "TNAU Farmer Schemes API",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "chat":   "/chat  [POST]",
            "docs":   "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "ready" if retrieval_chain is not None else "initializing",
        "chain_loaded": retrieval_chain is not None
    }

@app.post("/chat")
async def chat_endpoint(query: Query):
    try:
        response = retrieval_chain.invoke({"input": query.question})

        print("\n===== Retrieved Documents =====")
        for i, doc in enumerate(response["context"], start=1):
            print(f"\nDocument {i}")
            print(doc.page_content[:500])

        return {"answer": response["answer"]}

    except Exception as e:
        return {"error": str(e)}

    except Exception as e:
        print("Error:", e)
        return {"error": str(e)}