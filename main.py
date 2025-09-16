import os 
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    args = sys.argv[1:]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)
    user_prompt = " ".join(args)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    api_key = os.environ.get('GEMINI_API_KEY')
    client = genai.Client(api_key=api_key)

    if len(sys.argv) != 2:
        raise Exception('You have to ask a question as a argument!')

    model_response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages
    )
    prompt_token_count = model_response.usage_metadata.prompt_token_count
    response_token_count = model_response.usage_metadata.candidates_token_count

    print('Response: ')
    print(model_response.text)
    print(f'Prompt tokens: {prompt_token_count}')
    print(f'Response tokens: {response_token_count}')


if __name__ == "__main__":
    main()
