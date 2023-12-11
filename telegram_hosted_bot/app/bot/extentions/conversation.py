import os
from collections import deque
from dotenv import load_dotenv
import tiktoken
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
import logging


# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API credentials

class Conversation(deque):
    """
    The Conversation class represents a conversation history and provides methods for adding messages to the history, 
    getting the conversation history as a string, and summarizing the conversation history.
    """

    def __init__(self, initial_history=None, maxlen=15):
        self.history = deque(initial_history if initial_history else [], maxlen=maxlen)
        self.MAX_HISTORY_TOKENS = 3000

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})

    def get_conversation_str(self):
        return "\n".join(f"{message['role']}: {message['content']}" for message in self.history)


    def count_tokens(self, history):
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        total_tokens = 0
        for message in history:
            content = message.get('content', '')
            if not isinstance(content, str):
                raise ValueError("The 'content' field of each message must be a string.")
            tokenized_text = encoding.encode(content)
            total_tokens += len(tokenized_text)
        return total_tokens


    def summarize_text(self, history):
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": 'You are a helpful assistant that summarizes the conversation history to form your long term memory. Summarize the history but keep it under 500 tokens. '},
            *history,
        ])
        return response['choices'][0]['message']['content']

    def get_history_for_openai_api(self):
        return [{"role": message["role"], "content": message["content"]} for message in self.history]

    def summarize_conversation_history(self):
        history_for_api = self.get_history_for_openai_api()
        tokens_in_history = self.count_tokens(history_for_api)
        
        logging.info(f"History size: {len(self.history)}, tokens: {tokens_in_history}")

        # Summarize the conversation_str directly if it exceeds the token limit
        if tokens_in_history > self.MAX_HISTORY_TOKENS:
            summary = self.summarize_text(history_for_api)
            self.history.clear()
            self.add_message("assistant", summary)
            logging.info(f"Conversation history exceeded token limit. Summarized to: {summary}")
        


# Usage:
# conversation = Conversation()
# # Add your messages to the conversation
# conversation.add_message('User: Hi, how are you?')
# conversation.add_message('Bot: Hello! I am a bot designed to assist you. How can I help you today?')
# # ... add more messages as needed

# # Get the summary of the conversation
# print("Summary: ", conversation.get_conversation_summary())
