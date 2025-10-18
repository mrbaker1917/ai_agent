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
from call_function import call_function


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

    while True:
        response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
        if response.function_calls:
            for function_call in response.function_calls:
                messages.append(types.Content(
                    role="model",
                    parts=[
                        types.Part.from_function_call(
                            name=function_call.name,
                            args=function_call.args,
                        )
                    ],
                ))
                print(f"Calling function: {function_call.name}({function_call.args})")
                function_response = call_function(function_call, verbose=verbose)
                resp = function_response.parts[0].function_response.response
                text = str(resp.get("result") if isinstance(resp, dict) else resp)
                messages.append(types.Content(
                    role="user",
                    parts=[
                        types.Part(text=text)
                    ]
                ))
                messages.append(function_response)
                resp = function_response.parts[0].function_response.response
                text = resp.get("result") if isinstance(resp, dict) else resp
                if verbose:
                    print(f"-> {text}")
                else:
                    print(text)

            continue
        else:
            print(response.text)
            break

if __name__ == "__main__":
    main()
