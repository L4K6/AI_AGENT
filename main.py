import sys
import os
from config import *
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file,write_file

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    #user input that i can use
    input_argument = sys.argv[1:]
    
    if len(sys.argv) < 2:
        print("error: invalid input")
        sys.exit(1)

    user_prompt = " ".join(input_argument)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file
        ]
    )

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )
    verbose = "--verbose" in sys.argv
    if verbose:
        print("User prompt:", user_prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    

        
    if not response.function_calls:
        return response.text

    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)

        resp = function_call_result.parts[0].function_response.response
        if resp is None:
            raise RuntimeError("Missing function_response.response in tool content")

        if verbose:
            print(f"-> {resp}")
    
        
def call_function(function_call_part, verbose=False):
    name = function_call_part.name
    args = dict(function_call_part.args or {})
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:    
        print(f" - Calling function: {function_call_part.name}")
    dict_of_functions = {"get_file_content": get_file_content, "get_files_info": get_files_info, "run_python_file": run_python_file, "write_file": write_file}
    
    if name not in dict_of_functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"error": f"Unknown function: {name}"},
                )
            ],
        )

    kwargs = {"working_directory": "./calculator", **args}
    result = dict_of_functions[name](**kwargs)
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},
            )
        ],
    )

if __name__ == "__main__":
    main()
