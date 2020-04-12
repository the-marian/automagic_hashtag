import uvicorn
from fastapi import FastAPI

from utils import detect_labels_uri

app = FastAPI()


@app.get("/api/")
async def read_item(url: str):
    hash_tags = detect_labels_uri(url)
    return {"hash_tags": hash_tags}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
