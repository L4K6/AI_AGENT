import os
from config import *
from google import genai
from google.genai import types

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    absolute_working_path = os.path.normpath(os.path.abspath(working_directory))
    absolute_path_full = os.path.normpath(os.path.abspath(full_path))
    
    if os.path.commonpath([absolute_path_full, absolute_working_path]) != absolute_working_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(absolute_path_full):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(absolute_path_full, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            extra_char = f.read(1)
            
            if extra_char != "":
                return f'{file_content_string}[...File "{file_path}" truncated at 10000 characters]'
            
            return file_content_string
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name = "get_file_content",
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read from"
            ),
        },
        required=["file_path"]
    ),
)

    


    