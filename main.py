import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types


def main():
    print("Hello from ai-agent!")

    #Load virtual environment
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("API KEY NOT FOUND")

    #Get Gemini api key
    client = genai.Client(api_key=api_key)

    #Parser
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    # Conversation history
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # Generate response prompt
    response = client.models.generate_content(
        model = "gemini-2.5-flash", contents = messages
)   
    #Generate prompt and response token usage metadata
    usage = response.usage_metadata
    if usage is None:
        raise RuntimeError("Token usage is None")

    # Console outputs
    print(f"Prompt tokens: {usage.prompt_token_count}") # Print prompt token usage metadata
    print(f"Response tokens: {usage.candidates_token_count}") # Print response token usage metadata
    print(response.text) # Print response text


if __name__ == "__main__":
    main()
