import openai
import os
import logging

from const import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def call_openai(update, context) -> None:
    prompt = " ".join(context.args)
    logging.info(f"Received message from Telegram: {prompt}")
    response = generate_text(prompt)
    send_message_to_telegram(update, context, response)

def send_message_to_telegram(update, context, response) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

def generate_text(prompt, temperature=0.9, max_tokens=500) -> str:
    """ Generate text using OpenAI GPT-3 API. """
    
    logging.info(f"Sending message to OpenAI: {prompt}")
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    
    logging.debug(f"OpenAI response: {response}")

    return response["choices"][0]["text"]


if __name__ == "__main__":
    print(generate_text("what time is it now in Moscow?"))



