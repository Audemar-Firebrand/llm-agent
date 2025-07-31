import sys
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
from google import genai

client = genai.Client(api_key=api_key)
def main():
    if len(sys.argv) == 1:
        print("Error: please provide prompt")
        sys.exit(1)
    print("Hello from llm-agent!")
    response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=sys.argv[1])
    print(response.text)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
