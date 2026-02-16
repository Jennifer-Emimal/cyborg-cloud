from fastapi import FastAPI
from pydantic import BaseModel
import uuid
from datetime import datetime
import threading
import time

app = FastAPI()

jobs = {}

class ScanRequest(BaseModel):
    target: str

@app.get("/")
def home():
    return {"cyborg_cloud": "online"}

# submit job
@app.post("/submit")
def submit(request: ScanRequest):
    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        "target": request.target,
        "status": "queued",
        "created_at": datetime.utcnow().isoformat(),
        "verdict": None
    }

    return {"job_id": job_id, "status": "queued"}

# get result
@app.get("/result/{job_id}")
def result(job_id: str):
    if job_id not in jobs:
        return {"error": "job not found"}
    return jobs[job_id]


# ---------------------------
# Phase-2: execution worker
# ---------------------------

def analyze_target(target):
    # FAKE sandbox behaviour (temporary)
    time.sleep(5)  # simulate execution time

    if "virus" in target.lower():
        return "malicious"
    elif "unknown" in target.lower():
        return "suspicious"
    else:
        return "safe"


def worker():
    while True:
        for job_id, job in jobs.items():
            if job["status"] == "queued":
                job["status"] = "processing"

                verdict = analyze_target(job["target"])

                job["status"] = "completed"
                job["verdict"] = verdict

        time.sleep(2)


threading.Thread(target=worker, daemon=True).start()
