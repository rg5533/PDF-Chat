import openai
import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Set OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def generate_response(prompt: str, model: str = "gpt-4", max_tokens: int = 150) -> str:
    """
    Generates a response from OpenAI based on the provided prompt.

    :param prompt: The prompt to send to OpenAI.
    :param model: The OpenAI model to use.
    :param max_tokens: Maximum number of tokens in the response.
    :return: Generated response text.
    """
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error generating response from OpenAI: {e}")
        return "I'm sorry, I couldn't generate a response at this time."