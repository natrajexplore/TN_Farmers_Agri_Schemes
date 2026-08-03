from langchain_community.document_loaders import PlaywrightURLLoader, PyPDFLoader

# 1. Scraping HTML content from the TNAU site
url = "https://agritech.tnau.ac.in/expert_system/paddy/Schemes.html#cs"
html_loader = PlaywrightURLLoader(urls=[url])
html_docs = html_loader.load()

# 2. Loading PDFs (if you download or scrape PDF links)
pdf_loader = PyPDFLoader("path_to_downloaded_scheme.pdf")
pdf_docs = pdf_loader.load()

# Combine all scraped documents
all_documents = html_docs + pdf_docs

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import os

os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY"  # Replace with your actual OpenAI API key

# Split text into 1000-character chunks with a 200-character overlap
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(all_documents)

# Convert to embeddings and persist in a local folder called "chroma_db"
embeddings = OpenAIEmbeddings()
vector_store = Chroma.from_documents(
    documents=chunks, 
    embedding=embeddings, 
    persist_directory="./chroma_db"
)
print("Database built successfully!")

