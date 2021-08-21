import json
import os

VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')

def lambda_handler(event, context):
    
    response = {
        "statusCode": 200,
        "body": ""
    }
    
    try:
        if event['httpMethod'] == 'GET':
            if 'hub.verify_token' in event['queryStringParameters'] and event['queryStringParameters']['hub.verify_token'] == VERIFY_TOKEN:     
                response["body"] = event['queryStringParameters']['hub.challenge']
                print(response)
                return response
            else:
                response = {
                        "statusCode": 400,
                        "body":  "Wrong validation token"
                }
                print(response)
                return response
        elif event['httpMethod'] == 'POST':
            response["body"] = event["body"]
            print(response)
            return response
    except Exception as e:
        print(e)
        return e