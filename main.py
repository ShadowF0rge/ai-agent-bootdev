from email.mime import message
import os
import json
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import *

def main():
    print("Hello from my-ai-agent!")

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError("OPENROUTER_API_KEY is not set in the environment variables.")
    
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    tools=available_functions,
    #temperature=0
    )


    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        if response.usage.total_tokens > 0:
            print(f"Prompt tokens: {response.usage.total_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")




    message = response.choices[0].message

    if not message.tool_calls:
        print("Response:")
        print(message.content)
        return

    for tool_call in message.tool_calls:
        function_args = json.loads(tool_call.function.arguments or "{}")
        result_message = call_function(tool_call, verbose=args.verbose)
        if not result_message:
            raise RuntimeError(f"Function call failed for {tool_call.function.name} with arguments {function_args}")
        print(f"Function call result for {tool_call.function.name}:")
        print(result_message["content"])

if __name__ == "__main__":
    main()
