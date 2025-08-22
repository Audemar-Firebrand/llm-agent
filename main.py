import sys
import os
import argparse
from dotenv import load_dotenv
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
from google import genai

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

client = genai.Client(api_key=api_key)
def main():
    
    if len(sys.argv) == 1:
        print("Error: please provide prompt")
        sys.exit(1)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    user_prompt = args.prompt
    
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]
    print("Hello from llm-agent!")
    final_response = generate_content(client, messages, args.verbose)
    if final_response:
        print(final_response)

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
)
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


    if response.function_calls:
        function_call_result = call_function(response.function_calls[0], verbose)
        result = function_call_result.parts[0].function_response.response
        if not result:
            raise Exception("Error: failed to call function")
        if verbose:
            print(f" -> {result}")
        else:
            print(result)
    else:
        return response.text

if __name__ == "__main__":
    main()
