# TN_Farmers_Agri_Schemes
Tamil Nadu Agriculture Farmer Schemes RAG Application
This project is a Retrieval-Augmented Generation (RAG) application that
answers questions about Tamil Nadu Agriculture Farmer Schemes using
LangChain, ChromaDB, FastAPI, Streamlit, and OpenAI.

The application indexes agriculture scheme documents into a vector
database and retrieves relevant information before generating accurate
responses with an LLM.

Features
FastAPI backend for REST APIs

Streamlit web interface

LangChain Retrieval-Augmented Generation (RAG)

ChromaDB vector database

OpenAI GPT-4o Mini integration

OpenAI Embeddings

Environment variable management with .env

Health check endpoint

Interactive API documentation (Swagger UI)

Modular project structure

Technology Stack
Python 3.11+

FastAPI

Streamlit

LangChain

ChromaDB

OpenAI API

python-dotenv

Uvicorn

Project Structure
tnagri-rag-app/
│── main.py
│── app.py
│── ingest.py
│── requirements.txt
│── .env
│── chroma_db/
│── data/
│── README.md
Installation
Clone the repository.

Create a virtual environment.

python -m venv venv
Activate the environment.

Windows:

venv\Scripts\activate
Linux/macOS:

source venv/bin/activate
Install dependencies.

pip install -r requirements.txt
Environment Variables
Create a .env file in the project root.

OPENAI_API_KEY=your_openai_api_key
Build the Vector Database
Place the agriculture scheme documents inside the data folder and run:

python ingest.py
Run the FastAPI Backend
python -m uvicorn main:app --reload
Backend URL:

http://127.0.0.1:8000

Swagger UI: http://127.0.0.1:8000/docs

Run the Streamlit Frontend
streamlit run app.py
Sample Questions
What is the subsidy for purchasing a Tractor under Agricultural
Mechanisation?

What are the benefits of PM Kisan?

Who is eligible for the Micro Irrigation Scheme?

What subsidy is available for farm implements?

API Endpoint
POST /chat
Request

{
  "question": "What is the subsidy for tractor purchase?"
}
Response

{
  "answer": "..."
}
Troubleshooting
Verify the .env file contains a valid OPENAI_API_KEY.

Ensure chroma_db has been generated before starting the API.

Confirm all required Python packages are installed.

Check the FastAPI logs for runtime errors.

Future Enhancements
Hybrid Search (BM25 + Vector Search)

Reranking

Source citations

Conversation memory

Multilingual (Tamil + English)

LangSmith tracing and monitoring

Docker deployment

CI/CD pipeline

Author
Nataraj Angappan

Built as a GenAI RAG application for Tamil Nadu Agriculture Farmer
Schemes using LangChain and OpenAI.


