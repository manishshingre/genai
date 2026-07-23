from dotenv import load_dotenv
from server import app
import uvicorn

load_dotenv()

def main():
    uvicorn.run(app, host="127.0.0.2", port=8025)
    
main()
