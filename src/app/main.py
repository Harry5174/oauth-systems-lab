import uvicorn as uv
from fastapi import FastAPI

app = FastAPI(title="0Auth Identity lab")

@app.get("/health")
def health():
    return {"ok" : True}

def kickoff():
    """Entry point for uv run app"""
    uv.run(app="main:app", reload=True)