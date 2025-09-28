import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import SYSTEM_PROMPT

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file


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
        available_functions = types.Tool(
            function_declarations=[
                schema_get_files_info,
                schema_write_file,
                schema_run_python_file,
                schema_get_file_content,
            ]
        )

        model_response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT, tools=[available_functions]
            ),
        )

        if verbose:
            print(f"User prompt: {user_prompt}")

        if not model_response.function_calls:
            print("Response: ")
            return model_response.text

        for function_call_part in model_response.function_calls:
            print(
                f"Calling function: {function_call_part.name}({function_call_part.args})"
            )

        if verbose:
            print(f"Prompt tokens: {model_response.usage_metadata.prompt_token_count}")
            print(
                f"Response tokens: {model_response.usage_metadata.candidates_token_count}"
            )

    generateContent()


if __name__ == "__main__":
    main()
