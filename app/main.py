from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
