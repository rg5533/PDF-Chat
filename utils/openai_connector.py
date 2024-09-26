# utils/openai_connector.py

from openai import OpenAI
import os
from dotenv import load_dotenv
import logging

from utils.logger import setup_logging

# Initialize logging
setup_logging()

# Load environment variables
load_dotenv()

# Set OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logging.error("OPENAI_API_KEY not found in environment variables.")
    raise ValueError("The OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")

# Initialize OpenAI client with API key
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_response(prompt: str, model: str = "gpt-4", max_tokens: int = 150) -> str:
    """
    Generates a response from OpenAI based on the provided prompt.

    :param prompt: The prompt to send to OpenAI.
    :param model: The OpenAI model to use.
    :param max_tokens: Maximum number of tokens in the response.
    :return: Generated response text.
    """
    try:
        if not prompt.strip():
            error_msg = "Prompt is empty."
            logging.error(error_msg)
            raise ValueError(error_msg)

        logging.info("Sending prompt to OpenAI for response generation.")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        answer = response.choices[0].message.content.strip()
        logging.info("Received response from OpenAI.")
        return answer
    except Exception as e:
        logging.error(f"Error generating response from OpenAI: {e}")
        return "I'm sorry, I couldn't generate a response at this time."
