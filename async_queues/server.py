from unittest import result
import os
import sys

from fastapi import FastAPI, Query
from dotenv import load_dotenv

if __package__ in {None, ""}:
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from clients.rq_client import queue
from queues.worker import process_query

load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Server is up and running!"}
    
@app.post("/chat")
def chat(query: str = Query(..., description="The user query to process")):
    job = queue.enqueue("queues.worker.process_query", query)
    return {"job_id": job.id, "status": "Job enqueued successfully!"}

@app.get("/job-status")
def get_result(job_id: str = Query(..., description="The job ID to retrieve the result for")):
    job = queue.fetch_job(job_id)
    result = job.return_value()
    return {"job_id": job.id, "status": job.get_status(), "result": result}