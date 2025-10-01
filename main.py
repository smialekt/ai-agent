import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import SYSTEM_PROMPT, MAX_ITERATIONS

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function


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

    if verbose:
        print(f"User prompt: {user_prompt}")
        print("Response: ")

    i = 0
    try:
        while True:
            i += 1
            if i > MAX_ITERATIONS:
                print(f"Maximum iterations ({MAX_ITERATIONS}) reached.")
                sys.exit(1)

            final_response = GenerateContent(client, verbose, messages)

            if final_response:
                print("Final response:")
                print(final_response)
                break
    except Exception as e:
        print(f"Fatal exception occured while running agent:\n{e}")


def GenerateContent(client, verbose, messages):
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
        print(f"Prompt tokens: {model_response.usage_metadata.prompt_token_count}")
        print(
            f"Response tokens: {model_response.usage_metadata.candidates_token_count}"
        )

    if model_response.candidates:
        for candidate in model_response.candidates:
            messages.append(candidate.content)

    if not model_response.function_calls:
        return model_response.text

    function_responses = []
    for function_call_part in model_response.function_calls:
        content_response = call_function(function_call_part, verbose)
        function_response = content_response.parts[0].function_response.response
        if not function_response:
            raise Exception("Fatal exception. Terminating agent work")
        elif function_response.get("error"):
            print(function_response["error"])
        elif verbose:
            print(f" -> {function_response.get('result')}")

        function_responses.append(content_response.parts[0])

    messages.append(types.Content(role="user", parts=function_responses))


if __name__ == "__main__":
    main()
