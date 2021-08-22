import json
import os
import requests

VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')
PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')

def handle_message(sender_psid, received_message):
    response = {
      "text": f"You sent the message: {received_message}. Now send me an image!"
    }
    call_send_api(sender_psid, response)


def call_send_api(sender_psid, response):
    payload = {
        'recipient': {'id': sender_psid},
        'message': response,
        'messaging_type': 'RESPONSE'
    }
    headers = {'content-type': 'application/json'}

    url = 'https://graph.facebook.com/v2.6/me/messages?access_token={}'.format(PAGE_ACCESS_TOKEN)
    r = requests.post(url, json=payload, headers=headers)
    print(r.text)
      

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
            body = json.loads(event["body"])
            if body["object"] == 'page':
                for i in range(len(body["entry"])):
                    webhook_event = body["entry"][i]["messaging"]
                    sender_psid = webhook_event[i]['sender']['id']
                    message = webhook_event[i]['message']['text']
                    print('Sender PSID: ' + sender_psid)
                    response["body"] = json.dumps(sender_psid)
                    
                    handle_message(sender_psid, message)

            return response
    except Exception as e:
        print(e)
        return e