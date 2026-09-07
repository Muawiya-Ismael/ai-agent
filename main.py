import os, json, argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from functions.write_file import write_file
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.call_function import call_function, available_functions

parser = argparse.ArgumentParser(description="OpenRouter CLI FREE AI Agent")
parser.add_argument("user_prompt", type=str, help="User prompt for the OpenRouter CLI FREE AI AGent")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
    raise RuntimeError("OPENROUTER_API_KEY environment variable not found. Check your .env file.")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

for iteration in range(20):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    message = response.choices[0].message

    messages.append(message)

    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose=args.verbose)

            if not result_message.get("content"):
                raise Exception("Tool message content is empty")

            if args.verbose:
                print(f"-> {result_message['content']}")
            
            messages.append(result_message)
    else:
        print(message.content)
        break
else:
    sys.exit(1)