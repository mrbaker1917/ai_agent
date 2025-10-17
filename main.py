import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file

from functions.config import CHAR_LIMIT
from prompts import system_prompt


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
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file
    ]
)
    response = None
    for attempt in range(3):
        try:
            response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
            break  # If successful, exit the loop
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}", file=sys.stderr)
            time.sleep(2)  # Wait before retrying
    if response is None:
        print("Error: Failed to get a response from the API after multiple attempts.", file=sys.stderr)
        sys.exit(1)
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(response.text)

if __name__ == "__main__":
    main()
