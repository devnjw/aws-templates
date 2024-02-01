import os
import logging
import uvicorn
from fastapi import FastAPI
from mangum import Mangum

from db import init_aws_dynamodb, init_local_dynamodb, init_table

app = FastAPI()
handler = Mangum(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STAGE = os.environ.get("STAGE", "")
TABLE_NAME = "Items"

try:
    if STAGE == "local":
        dynamodb = init_local_dynamodb()
    else:
        dynamodb = init_aws_dynamodb()
    table = init_table(dynamodb, TABLE_NAME)
except Exception as e:
    logger.error(f"Error connecting to DynamoDB: {e}")
    raise e


@app.get("/")
def index():
    return "Hello World!"


@app.get("/items/")
async def read_items():
    response = table.scan()
    return response.get("Items", [])


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    response = table.get_item(Key={"uid": item_id})
    return response["Item"]


@app.post("/items/")
async def create_item(item: dict):
    response = table.put_item(Item=item)
    return response


@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    response = table.delete_item(Key={"uid": item_id})
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info", reload=True)
