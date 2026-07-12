from dotenv import load_dotenv
from os import getenv
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key= getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Vector Embeddings using Gemini/Google GenAI
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_rag",
    embedding=embeddings
)

# Take User Query
query = input("> ")

# Vector Similarity Search [query] in DB
search_results = vector_db.similarity_search(
    query=query
)

context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])

SYSTEM_PROMPT = f"""
    You are a helpfull AI Assistant who asnweres user query based on the available context
    retrieved from a PDF file along with page_contents and page number.

    You should only ans the user based on the following context and navigate the user
    to open the right page number to know more.

    Context:
    {context}
"""

chat_completion = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": query },
    ]
)

print(f"🤖: {chat_completion.choices[0].message.content}")