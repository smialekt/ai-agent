import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import SYSTEM_PROMPT


def main():
    load_dotenv()
    verbose = "--verbose" in sys.argv

    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    user_prompt = "".join(args)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    def generateContent():
        model_response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        )

        if verbose:
            print(f"User prompt: {user_prompt}")
        print("Response: ")
        print(model_response.text)
        if verbose:
            print(f"Prompt tokens: {model_response.usage_metadata.prompt_token_count}")
            print(
                f"Response tokens: {model_response.usage_metadata.candidates_token_count}"
            )

    generateContent()


if __name__ == "__main__":
    main()
