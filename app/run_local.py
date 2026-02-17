import dotenv

from lambda_function import lambda_handler
from dotenv import load_dotenv

load_dotenv()

class MockContext:
    def __init__(self):
        self.req = "local-req"

message = {
    "id": "123456",
    "permission": 1,
    "name": "Test Name",
    "email": "testmessage@test.com",
    "password": "#oIn#@1cbAzs)85",
    "date_birth": "10-10-2000",
    "method": "CREATE",
    "sites": {
        "candleio": {
            "Authorization": "Bearer ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890",
            "taskId": 123123123,
            "file": []
        }, 
        "spidermoon": {
            "taskId": 123123123,
            "prod": "verified",
            "mat": "protocol_1233213",
            "system": {"name": "theme", "value": "terror"},
            "files": []
        }, 
        "potatobooks": {
            "Authorization": "Bearer ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890",
            "taskId": 5656565656,
            "status": 5482354,
            "config": {"name": "theme", "value": "terror"},
            "file": []
        }}
}

if __name__ == "__main__":
    try:
        response = lambda_handler(event=message, context=MockContext)
    
    except Exception as e:
        print(e)