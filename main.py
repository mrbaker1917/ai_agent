import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

from functions.config import CHAR_LIMIT, system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    # print("Hello from ai-agent!")
    user_prompt = ""
    verbose = False
    # print(sys.argv)
    if len(sys.argv) > 1:
        user_prompt = sys.argv[1:]
        if "--verbose" in user_prompt:
            print("Verbose mode enabled")
            verbose = True
            user_prompt.remove("--verbose")
        user_prompt = " ".join(user_prompt)
    else:
        print("Error: Please provide input text as a command-line argument.", file=sys.stderr)
        sys.exit(1)
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]    
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages, config=types.GenerateContentConfig(system_instruction=system_prompt),)
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(response.text)

if __name__ == "__main__":
    main()
