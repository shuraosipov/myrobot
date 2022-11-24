import logging
import os

from telegram import Update
from telegram.ext import Updater,CallbackContext,CommandHandler,MessageHandler,Filters

from const import TELEGRAM_TOKEN
from auth import oauth_check_user_authentication, login
from commands import passwd, echo, caps


from extentions.openai_talk import call_openai
from extentions.lex_talk import call_lex
from extentions.list_google_calendars import calendar


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

if __name__ == "__main__":

    # Configure logging
    LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s",level=LOGLEVEL)
    logger = logging.getLogger()
    logger.setLevel(LOGLEVEL)

    # Instantiate telegram bot
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("login", login))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
    dispatcher.add_handler(CommandHandler("caps", caps))
    dispatcher.add_handler(CommandHandler("lex", call_lex))
    dispatcher.add_handler(CommandHandler("pass", passwd))
    dispatcher.add_handler(CommandHandler("calendar", calendar))
    dispatcher.add_handler(CommandHandler("openai", call_openai))

    # Handler for unknown commands. Should be the last one.
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
