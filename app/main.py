import argparse
from dotenv import load_dotenv
import os
import sys
import json

from openai import OpenAI

# 1. Find the folder where this script actually lives
script_dir = os.path.dirname(os.path.abspath(__file__))
# 2. Build the exact path to the .env file in that folder
env_path = os.path.join(script_dir, '.env')
# 3. Force dotenv to load from that specific path
load_dotenv(dotenv_path=env_path)
# print(env_path)

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    chat = client.chat.completions.create(
        # model="google/gemma-4-26b-a4b-it:free",
        model="anthropic/claude-haiku-4.5",
        messages=[{"role": "user", "content": args.p}],
        tools=[
                {
                    "type": "function",
                    "function": {
                    "name": "Read",
                    "description": "Read and return the contents of a file",
                    "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                        "type": "string",
                        "description": "The path to the file to read"
                        }
                    },
                    "required": ["file_path"]
                        }
                    }
                }
            ]
    )

    if not chat.choices or len(chat.choices) == 0:
        raise RuntimeError("no choices in response")

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    for tc in chat.choices[0].message.tool_calls or []:
        args = json.loads(tc.function.arguments)
        if tc.function.name == "Read":
            with open(args["file_path"]) as f:
                print(f.read())


if __name__ == "__main__":
    main()
