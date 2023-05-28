# Standard library imports
import logging
import os

# Third party imports
from telegram import __version__ as TG_VER
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Application-specific imports
from const import TELEGRAM_TOKEN
from handlers import ai, echo, hi, imagine, online, start, voice, help

# Version check
try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

### Enable logging.
LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.setLevel(LOGLEVEL)


def main() -> None:
    """Start the bot."""

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Define command mappings
    commands = {
        "start": start.handler,
        "help": help.handler,
        "hi": hi.handler,
        "online": online.handler,
        "ai": ai.handler,
        "sarah": ai.handler,
        "imagine": imagine.handler,
    }

    # Add command handlers
    for command, handler in commands.items():
        application.add_handler(CommandHandler(command, handler))

    # Add message handlers
    # on non command i.e message - echo the message on Telegram
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo.handler))

    # handling voice messages
    application.add_handler(MessageHandler(filters.VOICE, voice.handler))

    # print sticker details to the console
    # application.add_handler(MessageHandler(filters.Sticker.ALL, print_sticker_details))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
