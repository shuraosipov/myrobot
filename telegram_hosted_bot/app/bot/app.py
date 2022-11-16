import logging

from telegram import Update
from telegram.ext import Updater,CallbackContext,CommandHandler,MessageHandler,Filters

from const import TELEGRAM_TOKEN
from auth import oauth_check_user_authentication, check_auth_or_ask_for_login, login
from commands import call_lex, passwd, echo, caps, calendar


### Handlers for default commands
def start(update: Update, context: CallbackContext):
    """
    /start command is used to start the conversation with the bot.
    This is the only command that passes parameters to Telegram bot during initialization.
    It is used to pass the authorization code to the Bot.
    """
    oauth_check_user_authentication(update, context)
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def unknown(update: Update, context: CallbackContext):
    """Hanlder for unknown commands in Telegram."""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I don't know that command.")


### Handlers for custom commands
@check_auth_or_ask_for_login
def lex(update: Update, context: CallbackContext):
    call_lex(update, context)

if __name__ == "__main__":

    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s",
        level=logging.INFO
    )

    logger = logging.getLogger(__name__)

    # commands accessible without authentication
    start_handler = CommandHandler("start", start)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    passwd_handler = CommandHandler("pass", passwd)
    login_handler = CommandHandler("login", login)
    caps_handler = CommandHandler("caps", caps)
    

    # commands that require authentication
    lex_handler = CommandHandler("lex", lex)
    calendar_handler = CommandHandler("calendar", calendar)

    unknown_handler = MessageHandler(Filters.command, unknown)

    dispatcher.add_handler(login_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(caps_handler)
    dispatcher.add_handler(lex_handler)
    dispatcher.add_handler(passwd_handler)
    dispatcher.add_handler(calendar_handler)
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()
