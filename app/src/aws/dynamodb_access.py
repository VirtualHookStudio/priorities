import os
import boto3
import logging

class DynamoDBAccess:
    def __init__(self):
        self.region = os.getenv('AWS_REGION')
        self.table_name = os.getenv('DYNAMODB_TABLE_NAME')
        
        self.dynamodb = boto3.resource('dynamodb', region_name=self.region)
        self.table = self.dynamodb.Table(self.table_name)

    def put_item(self, item: dict):
        try:
            required_fields = ['id', 'permission', 'name', 'email', 'password', 'date_birth']
            for field in required_fields:
                if field not in item:
                    raise ValueError(f"Missing required field: {field}")

            self.table.put_item(Item=item)
            print(f"Item {item} inserted into {self.table_name}")
        except Exception as e:
            logging.error(f"Error inserting item: {e}")