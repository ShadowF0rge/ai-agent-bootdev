
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
        raise RuntimeError(
            "OPENROUTER_API_KEY is not set in the environment variables."
        )

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    # Agent loop (maximum 20 iterations)
    for iteration in range(20):

        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
            # temperature=0
        )

        if args.verbose and response.usage:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        message = response.choices[0].message

        # Add assistant message to conversation history
        messages.append(message)

        # Check if the model has finished its task
        if not message.tool_calls:
            print("Final response:")
            print(message.content)
            return

        # Execute requested function calls
        for tool_call in message.tool_calls:

            print(f"Calling function: {tool_call.function.name}")

            function_args = json.loads(
                tool_call.function.arguments or "{}"
            )

            result_message = call_function(
                tool_call,
                verbose=args.verbose
            )

            if not result_message:
                raise RuntimeError(
                    f"Function call failed for "
                    f"{tool_call.function.name} "
                    f"with arguments {function_args}"
                )

            # Add tool result to conversation history
            messages.append(result_message)

            if args.verbose:
                print(
                    f"Function call result for "
                    f"{tool_call.function.name}:"
                )
                print(result_message["content"])

    # Maximum iteration limit reached
    print(
        "Error: Maximum number of iterations (20) reached. "
        "The agent did not produce a final response."
    )

    print(f"Stopped after {iteration + 1} iterations.")
    print(f"Last message: {message.content}")

    raise SystemExit(1)


if __name__ == "__main__":
    main()
