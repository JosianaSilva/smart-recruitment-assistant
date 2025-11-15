from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/extract-text")
async def extract_text():
    return NotImplementedError("Text extraction not implemented yet.")