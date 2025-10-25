import os
from google import genai
from google.genai import types

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    absolute_path_full = os.path.abspath(full_path)
    absolute_working_path = os.path.abspath(working_directory)
    
    if os.path.commonpath([absolute_path_full, absolute_working_path]) != absolute_working_path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(absolute_path_full):
        return f'Error: "{directory}" is not a directory'
    
    
    try:
        lines = []
        list_of_files = os.listdir(absolute_path_full)
    
        for name in sorted(list_of_files):
            entry_path = os.path.join(absolute_path_full, name)
            size = os.path.getsize(entry_path)
            is_dir = os.path.isdir(entry_path)
            lines.append(f' - {name}: file_size={size} bytes, is_dir={is_dir}')
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


