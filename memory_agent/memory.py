from mem0 import Memory
from dotenv import load_dotenv
from os import getenv
from openai import OpenAI
from mem0.configs.base import MemoryConfig, LlmConfig, EmbedderConfig
from mem0.vector_stores.configs import VectorStoreConfig
import json

load_dotenv()
gemini_api_key = getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key= getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "google_genai",
        "config": {
            "api_key": gemini_api_key,
            "model": "gemini-embedding-2"
        }
    },
    "llm": {
        "provider": "google_genai",
        "config": {
            "api_key": gemini_api_key,
            "model": "gemini-3.6-flash"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333
        }
    }
}

custom_config = MemoryConfig(
    embedder=EmbedderConfig(
        provider="gemini",
        config={
            "model": "gemini-embedding-2"
        }
    ),
    llm=LlmConfig(
        provider="gemini",
        config={
            "model": "gemini-3-flash-preview"
        }
    ),
    vector_store=VectorStoreConfig(
        provider="qdrant",
        config={
            "host": "localhost",
            "port": 6333,
            "collection_name": "memories",      # Optional: custom name for your DB index
            "embedding_model_dims": 768         # CRITICAL: matches gemini-embedding-2 output
        }
    )
)

mem_client = Memory(config=custom_config)
while True:
    user_query = input("> ")

    search_memory = mem_client.search(query=user_query, 
                                      filters={ 'user_id': 'manish'})
    
    memories_stored = [
        f"ID: {mem.get("id")}\nMemory: {mem.get("memory")}" 
        for mem in search_memory.get("results")
    ]
    
    print("Fount Memories", memories_stored)
    
    SYSTEM_PROMPT = f"""
    Here is the context about the user:
    {json.dumps(memories_stored)}
    """
    
    response = client.chat.completions.create(
        model="gemini-3-flash-preview",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ]
    )

    ai_response = response.choices[0].message.content

    print("AI:", ai_response)

    mem_client.add(
        user_id="manish",
        messages= [
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": ai_response}
        ]
    )

    print("Memory has been saved....")