from os import getenv
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key= getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model = "gemini-3-flash-preview",
    messages = [
        { "role": "user", "content": "Hey there! I am Manish Shingre. Who are you?"}
    ]     
)

print(response.choices[0].message.content)