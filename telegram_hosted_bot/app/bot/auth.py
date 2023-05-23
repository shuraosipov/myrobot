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
    filters,
)

from requests_oauthlib import OAuth2Session

from const import (LOGIN_ENDPOINT, TOKEN_ENDPOINT, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

def base64_encode(string) -> str:
    return base64.b64encode(string.encode("utf-8")).decode("utf-8")


def decode_id_token(encoded_id_token) -> dict:

    return jwt.decode(
        encoded_id_token, 
        algorithms=["RS256"], 
        options={"verify_signature": False}
    )

def extract_attributes_from_id_token(decoded_id_token) -> dict:
    return {
        "email": decoded_id_token.get("email"),
        "username": decoded_id_token.get("cognito:username"),
        "first_name": decoded_id_token.get("given_name"),
        "last_name": decoded_id_token.get("family_name"),
        "google_access_token": decoded_id_token.get("custom:google_access_token"),
    }


def get_token(oauth, authorization_response):
    token = oauth.fetch_token(
        TOKEN_ENDPOINT,
        authorization_response=authorization_response,
        # Google specific extra parameter used for client
        # authentication
        client_secret=CLIENT_SECRET)

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
        "scope": "aws.cognito.signin.user.admin email openid phone profile https://www.googleapis.com/auth/calendar.readonly",
    }

    response = requests.post(token_endpoint, headers=headers, data=body)
    return response.json()


def oauth_get_user_info(authorization_code):
    response = oauth_get_token(TOKEN_ENDPOINT, authorization_code, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    id_token_attributes = extract_attributes_from_id_token(decode_id_token(response["id_token"]))
    
    first_name = id_token_attributes["first_name"]
    last_name = id_token_attributes["first_name"]
    email = id_token_attributes["first_name"]
    google_access_token = id_token_attributes["google_access_token"]

    return first_name, last_name, email, google_access_token

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
    first_name, last_name, email, google_access_token = oauth_get_user_info(auth_code)
    context.user_data["google_access_token"] = google_access_token
    text = f"🔐 You are logged in as {first_name} {last_name} ({email}).\n\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


# TODO add useful state


# def authorization_url(response_type="code", scope="aws.cognito.signin.user.admin+email+openid+phone+profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar.readonly", state="1234567890") -> str:
#     oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)

#     return f"{LOGIN_ENDPOINT}?client_id={CLIENT_ID}&response_type={response_type}&scope={scope}&redirect_uri={REDIRECT_URI}&state={state}"

def generate_authorization_url():
    scope = [
        'https://www.googleapis.com/auth/calendar.events.readonly',
        'https://www.googleapis.com/auth/calendar.readonly',
        'email',
        'openid',
        'phone',
        'profile',
        'aws.cognito.signin.user.admin',
    ]
    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=scope)
    authorization_url, state = oauth.authorization_url(LOGIN_ENDPOINT)
    return authorization_url

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
    google_access_token = context.user_data.get("google_access_token")

    state = update.message.text

    if access_token or google_access_token:
        text = f"🔐 You already logged in.\n\n"
    else:
        text = f"🔓 You are currently not logged in.\n\n"
        text += f"🔗 To log in, please visit the following URL: {generate_authorization_url()}\n"

    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
