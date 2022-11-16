import boto3
import string
import secrets
import logging
import requests
import json

from const import LEX_BOT_ID, LEX_BOT_ALIAS
from auth import check_auth_or_ask_for_login

def call_lex(update, context) -> None:
    """
    Invoke create_article_intent in Lex when /lex command is calle in Telegram.
    If no parameters are passed, the create_article_intent will be invoked by default.
    If parameters are passed, the create_article_intent will be invoked with the parameters.
    """
    if len(context.args) == 0:
        utterance = "call lambda"
    else:
        utterance = " ".join(context.args)

    lex_response = send_message_to_lex(utterance, LEX_BOT_ID, LEX_BOT_ALIAS)
    send_lex_reply_to_telegram(update, context, lex_response)


def send_message_to_lex(message, bot_id, bot_alias_id, locale_id="en_US") -> dict:
    lex = boto3.client("lexv2-runtime", region_name="us-east-1")
    
    logging.info(f"Sending message to Lex: {message}")
    
    response = lex.recognize_text(
        botId=bot_id,
        botAliasId=bot_alias_id,
        sessionId="123456",
        text=message,
        localeId=locale_id)
    return response


def format_lex_response(lex_response):
    """
    Format the Lex response to a string
    """
    for message in lex_response["messages"]:
        if message["contentType"] == "PlainText":
            return message["content"]


def send_lex_reply_to_telegram(update, context, lex_response) -> None:
    """
    Send the Lex response back to Telegram
    """
    for lex_message in lex_response["messages"]:
        if lex_message["contentType"] == "PlainText":
            context.bot.send_message(chat_id=update.effective_chat.id, text=lex_message["content"])


def passwd(update, context):
    """Sample command to generate a password.
    Can be called by passing /pass command in Telegram."""
    text = generate_password()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def generate_password() -> str:
    """Generate a ten-character alphanumeric password with at least one lowercase character,
    at least one uppercase character, and at least three digits"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = "".join(secrets.choice(alphabet) for i in range(10))
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password) >= 3
        ):
            break
    return password


def echo(update, context):
    """Echoing the user message back to the chat."""
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

@check_auth_or_ask_for_login
def caps(update, context):
    """Sample command to capitalize the message.
    Can be called by passing /caps <TEXT> command in Telegram."""
    text_caps = " ".join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

@check_auth_or_ask_for_login
def calendar(update,context):
    logging.info("Displaying list of calendars")
    calendars = list_google_calendars(context.user_data.get("google_access_token"))
    text = "🗓 Your Google Calendars:\n\n"
    
    for calendar_name in calendars:
        text += f"* {calendar_name}\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def list_google_calendars(access_token) -> list:
    """Get List of calendars from Google Calendar API using the access token from the user."""
    URL = "https://www.googleapis.com/calendar/v3/users/me/calendarList"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(URL, headers=headers)
    if response.status_code == 200:

        logging.info("Successfully retrieved calendars from Google Calendar API")
        calendars = []
        for calendar in json.loads(response.text)["items"]:
            if calendar["summary"] != "shuraosipov@gmail.com":
                calendars.append(calendar["summary"])
        return calendars
    else:
        logging.error(f"Failed to retrieve calendars from Google Calendar API. Error: {response.status_code}")
        return []

    
    
