import os
import boto3
import logging

logger = logging.getLogger(__name__)


def init_aws_dynamodb():
    logger.info("Connecting to AWS DynamoDB")
    dynamodb = boto3.resource("dynamodb")
    logger.info("Connected to AWS DynamoDB")
    return dynamodb


def init_local_dynamodb():
    logger.info("Connecting to local DynamoDB")
    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url=os.environ.get("DYNAMO_ENDPOINT"),
        region_name=os.environ.get("AWS_REGION"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    logger.info("Connected to local DynamoDB")
    return dynamodb


def init_table(dynamodb, table_name):
    logger.info(f"Connecting to DynamoDB table: {table_name}")
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
    return table
