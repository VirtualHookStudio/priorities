import os
import boto3
import logging

class SecretManagerAccess:
    def __init__(self):
        self.region = os.getenv('AWS_REGION')

        self.client = boto3.client('secretsmanager', region_name=self.region)

    def get_secret(self, secret_name: str) -> str:
        try:
            if not secret_name:
                secret_name = None
                
            if secret_name is None:
                raise ValueError(f"Secrets Manager failure")

            response = self.client.get_secret_value(SecretId=secret_name)
            secret = response['SecretString']
            
            return secret
        except Exception as e:
            logging.error(f"Error retrieving secret: {e}")
            return None