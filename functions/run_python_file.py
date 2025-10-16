import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
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
        result = subprocess.run(['python', real_full_path] + args, capture_output=True, text=True, timeout=30)
        return f"STDOUT: {result.stdout} Process exited with code {result.returncode}" if result.returncode == 0 else f'STDERR: {result.stderr} No output produced.'
    except Exception as e:
        return f"Error: executing Python file: {e}"
