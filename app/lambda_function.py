from datetime import datetime

from app.src.logs.log import Log
from app.src.users.users import User
from app.src.factories.site_factory import siteFactory
from app.src.aws.s3_access import S3Access

import json

def validate_event(event):
    required_fields = ['id', 'permission', 'name', 'email', 'password', 'date_birth', 'method', 'sites']
    for field in required_fields:
        if field not in event:
            return False
    
    valid_sites = {"candleio", "spidermoon", "potatobooks"}
    site_keys = set(event['sites'].keys())

    if not (1 <= len(site_keys) <= 3 and site_keys.issubset(valid_sites)):
        return False
        
    return True

def lambda_handler(event, context):
    if not validate_event(event):
        return {
            'statusCode': 400,
            'body': json.dumps({"error": "Invalid event data"})
        }

    user = User(event)

    log = Log()

    log.set_user(user)
    log.set_method(event['method'])

    sites = event['sites']

    response_sites = {}
    
    for site in sites:
        current_site_dict = sites[site]
        siteClass = siteFactory.get_site_instance(site)
        result_json = siteClass.requester(current_site_dict, { "user_id": event.get("id", ""), "user_email": event.get("email", "") })
        response_sites[site] = result_json
    
    file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + f"_{event.get('id', 'unknown_id')}.json"
    
    s3access = S3Access()
    s3access.upload_file(file_name, response_sites)

    return {
        'statusCode': 200,
        'body': json.dumps(response_sites)
    }