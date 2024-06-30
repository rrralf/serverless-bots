import json
from bot_logic import bot_handler

def lambda_handler(event, context):
    body = json.loads(event['body'])

    bot_handler.handle_event(body)

    return {
        'statusCode': 200,
        'body': json.dumps('Message processed successfully')
    }
