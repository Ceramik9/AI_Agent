import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import *
import sys

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
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # Conversation history
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # Generate response
    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )
        # Update candidates history
        for candidate in response.candidates:
            messages.append(candidate.content)

        #Generate prompt and response token usage metadata
        usage = response.usage_metadata
        if usage is None:
            raise RuntimeError("Token usage is None")

        # Console outputs
        if args.verbose is True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {usage.prompt_token_count}") # Print prompt token usage metadata
            print(f"Response tokens: {usage.candidates_token_count}") # Print response token usage metadata
        if response.function_calls:
            function_responses = []
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, args.verbose)
                if function_call_result.parts == []:
                    raise Exception
                if function_call_result.parts[0].function_response == None:
                    raise Exception
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception
                function_responses.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_responses))
        else:
            print("Final response:")
            print(response.text) # Print response text
            return
    print("Maximum iterations reached without a final response")
    sys.exit(1)


if __name__ == "__main__":
    main()

