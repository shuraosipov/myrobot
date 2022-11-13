"""
This module implements authentication functions for the bot.
"""
import base64
import requests
import jwt
import logging
import functools

from telegram import Update
from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    Filters,
)

from const import (LOGIN_ENDPOINT, TOKEN_ENDPOINT, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

def base64_encode(string) -> str:
    return base64.b64encode(string.encode("utf-8")).decode("utf-8")


def decode_jwt(encoded_id_token) -> dict:

    decoded_id_token = jwt.decode(
        encoded_id_token, 
        algorithms=["RS256"], 
        options={"verify_signature": False}
    )

    user_info = {
        "email": decoded_id_token.get("email"),
        "username": decoded_id_token.get("cognito:username"),
        "first_name": decoded_id_token.get("given_name"),
        "last_name": decoded_id_token.get("family_name"),
    }
    return user_info


def oauth_get_token(token_endpoint, auth_code, client_id, client_secret, redirect_uri) -> dict:
    """
    This function uses the auth code to get the access token from the token endpoint
    It returns a dict containing access_token, id_token and refresh_token.
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {base64_encode(client_id + ':' + client_secret)}",
    }

    body = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": redirect_uri,
        "scope": "aws.cognito.signin.user.admin email openid phone profile",
    }

    response = requests.post(token_endpoint, headers=headers, data=body)
    return response.json()

def oauth_get_user_info(authorization_code):
    response = oauth_get_token(TOKEN_ENDPOINT, authorization_code, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    id_token = response["id_token"]
    first_name = decode_jwt(id_token)["first_name"]
    last_name = decode_jwt(id_token)["last_name"]
    email = decode_jwt(id_token)["email"]

    return first_name, last_name, email

def oauth_check_user_authentication(update: Update, context: CallbackContext):
    """
    This needed to check parameter passed using deep linking to /start command.
    """
    try:
        auth_code = context.args[0]
    except IndexError:
        logging.info("No auth code found in context.args")
        return False

    context.user_data["auth_code"] = auth_code
    first_name, last_name, email = oauth_get_user_info(auth_code)
    text = f"🔐 You are logged in as {first_name} {last_name} ({email}).\n\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


# TODO add useful state
def oauth_login_url(response_type="code", scope="aws.cognito.signin.user.admin+email+openid+phone+profile", state="1234567890") -> str:
    return f"{LOGIN_ENDPOINT}?client_id={CLIENT_ID}&response_type={response_type}&scope={scope}&redirect_uri={REDIRECT_URI}&state={state}"


def check_auth_or_ask_for_login(func):
    """
    Decorator: checks if user is authenticated, if not, forwards user to a login screen.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        update: Update = args[0]
        context: CallbackContext = args[1]
        if not check_auth(context):
            return login(update, context)
        return func(*args, **kwargs)
    return wrapper

def check_auth(context: CallbackContext):
    auth_code = context.user_data.get("auth_code")

    if auth_code:
        logging.info("Auth code exists")
        return True
    else:
        logging.info("Auth code does not exist.. Redirecting to login page...")
        return False

def login(update: Update, context: CallbackContext) -> None:
    access_token = context.user_data.get("access_token")

    state = update.message.text

    if access_token:
        text = f"🔐 You already logged in.\n\n"
    else:
        text = f"🔓 You are currently not logged in.\n\n"
        text += f"🔗 To log in, please visit the following URL: {oauth_login_url(state=state)}\n"

    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
