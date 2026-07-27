from dotenv import load_dotenv
from openai import OpenAI
from os import getenv

load_dotenv()

client = OpenAI(
    api_key= getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

chat_completion = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            { "role": "user", 
                "content": [
                    { "type": "text", "text": "Generate a caption for this image in about 50 words." },
                    { "type": "image_url", "image_url": {"url": "https://in.pinterest.com/pin/scenery-drawing-for-kids--822188475765705964/" } }
                ] }
        ]
    )
    
print(chat_completion.choices[0].message.content)