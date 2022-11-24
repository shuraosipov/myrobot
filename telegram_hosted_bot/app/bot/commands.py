import string
import secrets
import logging


def passwd(update, context):
    """Sample command to generate a password.
    Can be called by passing /pass command in Telegram."""
    logging.info("Received /pass command from Telegram. Generating password.")
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

def caps(update, context):
    """Sample command to capitalize the message.
    Can be called by passing /caps <TEXT> command in Telegram."""
    text_caps = " ".join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

