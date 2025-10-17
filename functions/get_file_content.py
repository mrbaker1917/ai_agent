import os
import types
from google import genai
from google.genai import types

from functions.config import CHAR_LIMIT

# Import config from parent directory
def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    # Make sure the full_path is within the working directory to prevent directory traversal attacks
    real_full_path = os.path.realpath(full_path)
    real_working_dir = os.path.realpath(working_directory)
    if not real_full_path.startswith(real_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    # Check if the path is a valid file
    if not os.path.isfile(real_full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    with open(real_full_path, 'r') as file:
        content = file.read()
        if len(content) > CHAR_LIMIT:
            return content[:CHAR_LIMIT] + f'[...File "{file_path}" truncated at {CHAR_LIMIT} characters]'

    return content

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    )
)