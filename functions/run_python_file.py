import os
import subprocess
import sys
def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    absolute_full_path = os.path.normpath(os.path.abspath(full_path))
    absolute_working_path = os.path.normpath(os.path.abspath(working_directory))

    if os.path.commonpath([absolute_full_path, absolute_working_path]) != absolute_working_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(absolute_full_path):
        return f'Error: File "{file_path}" not found.'

    if not absolute_full_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        completed_process = subprocess.run([sys.executable, absolute_full_path, *args],cwd=absolute_working_path, text=True, timeout=30, capture_output=True)
        
        process_output = completed_process.stdout or ""
        process_error = completed_process.stderr or ""
        process_exit = completed_process.returncode
        
        return_message = [f"STDOUT: {process_output}, STDERR: {process_error}"]

        if process_output.strip() == None:
            return "No output produced."
        
        if process_exit != 0:
            return_message.append(f"Process exited with code {process_exit}")

        return " ".join(return_message) 
        
    except Exception as e:
        return f"Error: executing Python file: {e}"

        