from google import genai
from google.genai import types 
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file

FUNCTIONS = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
}

def call_function(function_call_part, verbose=False):
    # if verbose:
        # print("DEBUG name:", function_call_part.name)
        # print("DEBUG args:", function_call_part.args, type(function_call_part.args))
    # Here you would implement the actual function calling logic
    # For example, if function_call_part.name == "get_files_info", you would call that function
    print(f" - Calling function: {function_call_part.name}")

    args = dict(function_call_part.args)
    args["working_directory"] = "./calculator"
    # print(f"here are the args: {args}")
    # if "path" in args and "file_path" not in args:
    #     args["file_path"] = args.pop("path")
    if FUNCTIONS.get(function_call_part.name) is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    result = FUNCTIONS[function_call_part.name](**args)
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=FUNCTIONS.get(function_call_part.name).__name__,
            response={"result": result},
        )
    ],
)