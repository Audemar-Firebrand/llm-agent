import sys
import os
import argparse
from dotenv import load_dotenv
from google.genai import types
from functions.get_files_info import schema_get_files_info

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
from google import genai

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[schema_get_files_info,
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
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
)
    if response.function_calls:
        print(f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args})")
    print(response.text)
    if args.verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
