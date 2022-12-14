import os

# Manage loglevel centrally
LOGLEVEL = os.environ["LOGLEVEL"]

# Telegram bot token
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]

# OAuth2 with Congito Authorization Server
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REDIRECT_URI = os.environ["REDIRECT_URI"]
AUTHORIZATION_SERVER_URL = os.environ["AUTHORIZATION_SERVER_URL"]
TOKEN_ENDPOINT = AUTHORIZATION_SERVER_URL + "/oauth2/token"
LOGIN_ENDPOINT = AUTHORIZATION_SERVER_URL + "/login"

# Lex
LEX_BOT_ID = os.environ["LEX_BOT_ID"]
LEX_BOT_ALIAS = os.environ["LEX_BOT_ALIAS"]

# OpenAI
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]