import json
import os
import requests
import boto3

# reuse client connection as global
lex = boto3.client('lexv2-runtime')

# read environment variables
TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = os.environ['TELEGRAM_BASE_URL'] + TOKEN
BOT_ID = os.environ['LEX_BOT_ID']
BOT_ALIAS_ID = os.environ['LEX_BOT_ALIAS_ID']


def send_message_to_lex(message, bot_id=BOT_ID, bot_alias_id=BOT_ALIAS_ID, locale_id='en_US') -> dict:
    response = lex.recognize_text(
        botId=bot_id,
        botAliasId=bot_alias_id,
        sessionId='123456',
        text=message,
        localeId=locale_id
    )
    return response

def send_message_to_telegram(message, chat_id, base_url=BASE_URL) -> None:
    data = {
        "text": message, 
        "chat_id": chat_id
    }
    url = base_url + "/sendMessage"
    requests.post(url, data)


def send_multiple_messages_to_telegram(lex_messages, chat_id) -> None:
    for message in lex_messages:
        send_message_to_telegram(message['content'], chat_id)
    

def lambda_handler(event, context):
    # print(json.dumps(event))

    # get message from telegram
    data = json.loads(event["body"])
    message = str(data["message"]["text"])
    chat_id = data["message"]["chat"]["id"]
    first_name = data["message"]["chat"]["first_name"]


    try:

        if "/start" in message:
            send_message_to_telegram(f"Hi {first_name}, welcome to Typewriter AI!", chat_id)
        else:
            response = send_message_to_lex(message, bot_id=BOT_ID, bot_alias_id=BOT_ALIAS_ID)
            send_multiple_messages_to_telegram(response['messages'], chat_id)

        return {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
        }
    except Exception as e:
        print(e)
        raise e