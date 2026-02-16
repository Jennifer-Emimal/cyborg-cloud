from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ScanRequest(BaseModel):
    target: str

@app.get("/")
def home():
    return {"cyborg_cloud": "online"}

@app.post("/scan")
def scan(request: ScanRequest):
    # temporary fake analysis logic
    if "virus" in request.target.lower():
        return {"verdict": "malicious"}
    elif "unknown" in request.target.lower():
        return {"verdict": "suspicious"}
    else:
        return {"verdict": "safe"}
