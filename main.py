from fastapi import FastAPI
from pydantic import BaseModel
import uuid
from datetime import datetime

app = FastAPI()

# temporary in-memory job database
jobs = {}

class ScanRequest(BaseModel):
    target: str

@app.get("/")
def home():
    return {"cyborg_cloud": "online"}

# Phase-1: ingestion endpoint
@app.post("/submit")
def submit(request: ScanRequest):
    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        "target": request.target,
        "status": "queued",
        "created_at": datetime.utcnow().isoformat(),
        "verdict": None
    }

    return {
        "job_id": job_id,
        "status": "queued"
    }

# check job result
@app.get("/result/{job_id}")
def result(job_id: str):
    if job_id not in jobs:
        return {"error": "job not found"}

    return jobs[job_id]
