import os
import boto3
import json
import logging

from app.src.logs.log import Log

class S3Access:
    def __init__(self):
        self.region = os.getenv('AWS_REGION')
        self.bucket_name = os.getenv('S3_BUCKET_NAME')
        self.file_path = os.getenv('FILE_PATH')

        self.s3 = boto3.client('s3', region_name=self.region)
        

    def upload_file(self, file_name: str, res: str):
        if not res:
            res = None

        if not file_name or not file_name.endswith(".json"):
            file_name = None

        try:
            if file_name is None or res is None:
                raise ValueError(f"Missing required field: file_name or res")

            log = Log()

            object_dict = {
                'user': log.get_user(),
                'method': log.get_method(),
                'time_info': log.get_time_info(),
                'responses': res
            }

            object_json = json.dumps(object_dict)

            self.s3.put_object(Bucket=self.bucket_name, Key=file_name, Body=object_json)
            print(f"File {file_name} uploaded to {self.bucket_name}/{file_name}")
        except Exception as e:
            logging.error(f"Error uploading file to S3: {e}")