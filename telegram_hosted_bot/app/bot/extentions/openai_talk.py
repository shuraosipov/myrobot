import logging
import openai
from openai.error import Timeout

from const import OPENAI_API_KEY


def call_openai(update, context) -> None:
    prompt = " ".join(context.args)

    logging.debug(f"Received message from Telegram: {prompt}")
    response = generate_text(prompt)
    send_message_to_telegram(update, context, response)


def send_message_to_telegram(update, context, response) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)


def generate_text(prompt, temperature=0.9, max_tokens=500, timeout_sec=5) -> str:
    """
    Generate text using OpenAI GPT-3 API.
    """
    openai.api_key = OPENAI_API_KEY
    logging.debug(f"Sending message to OpenAI: {prompt}")

    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            request_timeout=timeout_sec,
        )

        logging.debug(f"OpenAI response: {response}")
        return response["choices"][0]["text"]

    except Timeout as e:
        logging.error(f"OpenAI timeout: {e}")
        raise f"OpenAI timeout: {e}"
    except Exception as e:
        logging.error(f"OpenAI error: {e}")
        raise "Unexpected error occured while calling OpenAI API."


if __name__ == "__main__":
    print(generate_text("what time is it now in Moscow?"))
