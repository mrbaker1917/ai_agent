import os
import subprocess
import types
from google import genai
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    full_path = os.path.join(working_directory, file_path)
    # Make sure the full_path is within the working directory to prevent directory traversal attacks
    real_full_path = os.path.realpath(full_path)
    real_working_dir = os.path.realpath(working_directory)
    if not real_full_path.startswith(real_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    # Check if the path is a valid file
    if not os.path.isfile(real_full_path):
        return f'Error: File "{file_path}" not found.'
    if not real_full_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    # Run the Python file
    try:
        print(f"Executing Python file: {real_full_path} with args: {args}, working_directory: {working_directory}")
        cmd = ["python3", "-u", file_path]
        if args:
            cmd.extend(args)
        result = subprocess.run(cmd, cwd=working_directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
        # print(f"cmd: {cmd}, cwd: {working_directory}")
        output = (result.stdout or "") + (result.stderr or "")
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of string arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)