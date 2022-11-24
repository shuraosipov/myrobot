import boto3
import logging

from const import LEX_BOT_ID, LEX_BOT_ALIAS
from auth import check_auth_or_ask_for_login

@check_auth_or_ask_for_login
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