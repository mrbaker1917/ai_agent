import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    # Make sure the full_path is within the working directory to prevent directory traversal attacks
    real_full_path = os.path.realpath(full_path)
    real_working_dir = os.path.realpath(working_directory)
    if not real_full_path.startswith(real_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # Check if the path is a valid directory
    if not os.path.isdir(real_full_path):
        return f'Error: "{directory}" is not a directory'
    
    listdir = os.listdir(real_full_path)
    files_info = ""
    for item in listdir:
        item_path = os.path.join(real_full_path, item)
        files_info += f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}\n"
    return files_info

