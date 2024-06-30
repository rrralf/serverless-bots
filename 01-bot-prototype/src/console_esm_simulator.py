import json

def get_aws_event(chat_id, text, user_nick):
    req_json = {
        'update_id': 789563375,
        'message': {
            'message_id': 216,
            'from': {
                'id': chat_id,
                'is_bot': False,
                'first_name': 'user-first-name',
                'username': user_nick,
                'language_code': 'en'
            },
            'chat': {
                'id': chat_id,
                'first_name': 'user-first-name',
                'username': user_nick,
                'type': 'private'
            },
            'date': 1719677266,
            'text': text,
            'entities': [
                {'offset': 0, 'length': 13, 'type': 'bot_command'}
            ]
        }
    }

    aws_event = {
        "version": "2.0",
        "routeKey": "ANY /webhook",
        "rawPath": "/webhook",
        "rawQueryString": "",
        "headers": {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "content-length": "394",
            "content-type": "application/json",
            "host": "ng79a68gph.execute-api.eu-central-1.amazonaws.com",
            "postman-token": "cbdf81be-3707-4383-b5b4-0d6fc71940e6",
            "user-agent": "PostmanRuntime/7.39.0",
            "x-amzn-trace-id": "Root=1-6676d931-3d6752cf6f055cd810e8f4e2",
            "x-forwarded-for": "185.244.156.97",
            "x-forwarded-port": "443",
            "x-forwarded-proto": "https"
        },
        "requestContext": {
            "accountId": "126459111222",
            "apiId": "ng79a68gph",
            "domainName": "ng79a68gph.execute-api.eu-central-1.amazonaws.com",
            "domainPrefix": "ng79a68gph",
            "http": {
                "method": "POST",
                "path": "/webhook",
                "protocol": "HTTP/1.1",
                "sourceIp": "185.244.156.97",
                "userAgent": "PostmanRuntime/7.39.0"
            },
            "requestId": "Zxbfujs1liAEJZQ=",
            "routeKey": "ANY /webhook",
            "stage": "$default",
            "time": "22/Jun/2024:14:01:21 +0000",
            "timeEpoch": 1719064881172
        }, ''
           "body": json.dumps(req_json),
        "isBase64Encoded": False
    }

    return aws_event