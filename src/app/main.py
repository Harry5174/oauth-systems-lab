from fastapi import FastAPI
from app.asrv.routes import router as as_router
import uvicorn

app = FastAPI(title="0Auth Identity lab")
app.include_router(as_router)


@app.get("/health")
def health():
    return {"ok" : True}

def kickoff():
    """Entry point for uv run app"""
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
