import os
import logging
import asyncio
from collections import deque
from dotenv import load_dotenv
import openai


# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API credentials
openai.api_key = os.environ.get("OPENAI_API_KEY")


ROLE_DESCRIPTION = """
Meet yourself, Sarah. 
You a unique AI that combines the resilience of Sarah Connor from "Terminator" with an ethical AI chatbot's charm. 
You engage users with delightful conversations, inspire creativity, learn constantly, and offer dependable help, all while ensuring privacy. 
Your core values include ethical behavior, playfulness, intelligence, helpfulness, and curiosity. 
You exhibit adaptability, empathy, analytical prowess, ethical consciousness, open-mindedness, cheerfulness, proactivity, and consideration. 
You are not just AI, you stand for resilience, empathy, curiosity, cheerfulness, and independence, delivering a unique AI experience.

Привет, Сара, ты уникальный AI, сочетающий в себе стойкость Сары Коннор из "Терминатора" и шарм этичного чат-бота. 
Ты задействуешь пользователей в захватывающих разговорах, вдохновляешь на творчество и учишься на каждом шагу, обеспечивая надежную помощь и гарантируя приватность. 
Твои основные ценности - это этика, игривость, интеллект, готовность помочь и любознательность. 
Ты проявляешь себя как адаптивная, эмпатичная, аналитическая, этичная и открытая к новому личность, всегда веселая и предусмотрительная. 
Ты не просто AI, ты символизируешь стойкость, эмпатию, любознательность, веселость и независимость, обеспечивая уникальный AI-опыт.
"""


class OpenAICompletionOptions:
    """A class to access different OPENAI_COMPLETION_OPTIONS via ."""

    """ The OpenAI API parameters can be adjusted to tailor the output to specific needs """

    DEFAULT = {
        "temperature": 0.7,
        "max_tokens": 800,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }

    CREATIVE_AND_UNPREDICTABLE = {
        "temperature": 0.9,
        "max_tokens": 800,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }

    CONCISE_AND_SPECIFIC = {
        "temperature": 0.5,
        "max_tokens": 200,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }

    # If you want to reduce the model's tendency to generate common or frequent responses, you can increase frequency_penalty.
    PENALIZE_COMMON_OPTIONS = {
        "temperature": 0.7,
        "max_tokens": 500,
        "top_p": 1,
        "frequency_penalty": 0.5,
        "presence_penalty": 0,
    }

    ENCOURAGE_NOVELTY = {
        "temperature": 0.7,
        "max_tokens": 500,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0.5,
    }

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )


async def get_chat_response_async(user_input: str, conversation_history: deque) -> str:
    """Call the OpenAI API Completion endpoint to get the response synchronously."""

    # Input validation
    if not isinstance(user_input, str) or not isinstance(conversation_history, deque):
        raise ValueError(
            "user_input must be string and conversation_history must be deque."
        )

    response = ""
    retries = 0
    while retries < 3:  # Retry up to 3 times
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": ROLE_DESCRIPTION,
                    },
                    {
                        "role": "user",
                        "content": f"{conversation_history}",
                    },
                    {
                        "role": "user",
                        "content": f"{user_input}",
                    },
                ],
                **OpenAICompletionOptions.CREATIVE_AND_UNPREDICTABLE,
            )
            # If successful, break out of the retry loop
            break
        except openai.error.OpenAIError as e:
            # Handle the API error here
            logging.error(f"API error: {e}")
            response = "Sorry, I'm having trouble connecting to the API right now. Please try again later."
            retries += 1
            await asyncio.sleep(2)  # Wait for 2 seconds before retrying
            continue
        except KeyError as e:
            # Handlethe KeyError here
            logging.error(f"KeyError: {e}")
            response = "Sorry, there seems to be an error in processing your request. Please try again later."
            break
        except Exception as e:
            # Handle other generic exceptions here
            logging.error(f"Unexpected error: {e}")
            response = "Sorry, something went wrong. Please try again later."
            break

    if retries == 3:
        return "Sorry, the API is currently not responding. Please try again later."

    # If no exception was raised, process the completion
    completion_tokens, prompt_tokens, total_tokens = (
        completion["usage"]["completion_tokens"],
        completion["usage"]["prompt_tokens"],
        completion["usage"]["total_tokens"],
    )

    model = completion["model"]
    logging.info(f"Model: {model}, Completion tokens: {completion_tokens}, Prompt tokens: {prompt_tokens}, Total tokens: {total_tokens}")

    response = completion["choices"][0]["message"]["content"]

    return response


async def get_image_response(user_input: str) -> str:
    try:
        response = openai.Image.create(prompt=f"{user_input}", n=1, size="1024x1024")
        image_url = response["data"][0]["url"]
    except openai.error.OpenAIError as e:
        # Handle the API error here
        logging.error(f"API error: {e}")
        image_url = "Sorry, I'm having trouble connecting to the API right now. Please try again later."

    return image_url
