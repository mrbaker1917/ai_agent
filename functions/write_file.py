import os

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    # Make sure the full_path is within the working directory to prevent directory traversal attacks
    real_full_path = os.path.realpath(full_path)
    real_working_dir = os.path.realpath(working_directory)
    if not real_full_path.startswith(real_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    # Write the content to the file
    with open(real_full_path, 'w') as file:
        file.write(content)

    return f'Success: Wrote to "{file_path}"'
    return content