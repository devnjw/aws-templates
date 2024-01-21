import logging
import uvicorn
from fastapi import FastAPI
from mangum import Mangum

import boto3

app = FastAPI()
handler = Mangum(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    dynamodb = boto3.resource("dynamodb")
    table_name = "Recipes"
    if table_name not in [table.name for table in dynamodb.tables.all()]:
        dynamodb.create_table(
            TableName=table_name,
            AttributeDefinitions=[
                {"AttributeName": "uid", "AttributeType": "S"},
            ],
            KeySchema=[
                {"AttributeName": "uid", "KeyType": "HASH"},
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 10,
                "WriteCapacityUnits": 10,
            },
        )
    table = dynamodb.Table(table_name)
    logger.info(f"Connected to DynamoDB table: {table_name}")
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
