import os
def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    absolute_full_path = os.path.normpath(os.path.abspath(full_path))
    absolute_working_path = os.path.normpath(os.path.abspath(working_directory))
    
    if os.path.commonpath([absolute_full_path, absolute_working_path]) != absolute_working_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    #gives you name of the directory in the path (use on absolute paths)
    new_dir_path = os.path.dirname(absolute_full_path)
    
    try:
        if not os.path.exists(absolute_full_path):
            
            os.makedirs(new_dir_path, exist_ok=True)

    
        with open(absolute_full_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"