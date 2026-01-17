from fastapi import FastAPI

app = FastAPI(title="0Auth Identity lab")

@app.get("/health")
def health():
    return {"ok" : True}

