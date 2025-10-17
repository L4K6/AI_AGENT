import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    #user input that i can use
    input_argument = sys.argv[1]
    
    if len(sys.argv) < 2:
        print("error: invalid input")
        sys.exit(1)

    user_prompt = " ".join(input_argument)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]


    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages
    )
    verbose = "--verbose" in sys.argv
    if verbose:
        print("User prompt:", user_prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:")
    print(response.text)

    


if __name__ == "__main__":
    main()
