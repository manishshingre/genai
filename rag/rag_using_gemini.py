from os import getenv
from dotenv import load_dotenv
from pathlib import Path
from typing import List

from google import genai
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

pdf_path = Path(__file__).parent / "nodejs.pdf"

# load the file
loader = PyPDFLoader(file_path=pdf_path)
pages = loader.load()

# split the pages into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)
chunks = text_splitter.split_documents(documents=pages)

# Vector Embeddings using Gemini/Google GenAI
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")

# Using [embedding_model] create embeddings of [chunks] and store in DB
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    url="http://localhost:6333",
    collection_name="learning_rag",
    embedding=embeddings,
)

print("Indexing of Documents Done...")