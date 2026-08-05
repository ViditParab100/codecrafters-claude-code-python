import argparse
from email.mime import message
from dotenv import load_dotenv
import os
import sys
import json

from openai import OpenAI
from sarvamai import SarvamAI

# 1. Find the folder where this script actually lives
script_dir = os.path.dirname(os.path.abspath(__file__))
# 2. Build the exact path to the .env file in that folder
env_path = os.path.join(script_dir, '.env')
# 3. Force dotenv to load from that specific path
load_dotenv(dotenv_path=env_path)
# print(env_path)

API_KEY = os.getenv("OPENROUTER_API_KEY")
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")
    if not SARVAM_API_KEY:
        raise RuntimeError("SARVAM_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    sarvam_client = SarvamAI(api_subscription_key=SARVAM_API_KEY)

    messages=[{"role": "user", "content": args.p}]

    while True:
        chat = sarvam_client.chat.completions(
            # model="google/gemma-4-26b-a4b-it:free",
            # model="anthropic/claude-haiku-4.5",
            model="sarvam-105b",
            messages=messages,
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
                },
                {
                    "type": "function",
                    "function": {
                        "name": "Write",
                        "description": "Write content to a file",
                        "parameters": {
                        "type": "object",
                        "required": ["file_path", "content"],
                        "properties": {
                            "file_path": {
                            "type": "string",
                            "description": "The path of the file to write to"
                            },
                            "content": {
                            "type": "string",
                            "description": "The content to write to the file"
                            }
                        }
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "Bash",
                        "description": "Execute a shell command",
                        "parameters": {
                        "type": "object",
                        "required": ["command"],
                        "properties": {
                            "command": {
                            "type": "string",
                            "description": "The command to execute"
                            }
                        }
                        }
                    }
                }
            ]
        )

        if not chat.choices or len(chat.choices) == 0:
            raise RuntimeError("no choices in response")

        response = chat.choices[0].message
        response_message = chat.choices[0].message
        message_dict = {
            "role": response_message.role,
            "content": response_message.content,
        }

        if hasattr(response_message, "tool_calls") and response_message.tool_calls:
            message_dict["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in response_message.tool_calls
            ]

        messages.append(message_dict)
        if not message_dict.get("tool_calls"):
            print(response.content)
            break  

        # You can use print statements as follows for debugging, they'll be visible when running tests.
        print("Logs from your program will appear here!", file=sys.stdout)

        
        for tc in response_message.tool_calls:
            args_dict = json.loads(tc.function.arguments)
            if tc.function.name == "Read":
                with open(args_dict["file_path"], "r") as f:
                    result = f.read()
                    messages.append(
                        {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": result
                    }
                    )
            elif tc.function.name == "Write":
                if not os.path.exists(args_dict["file_path"]):
                    with open(args_dict["file_path"], "w") as f:
                        f.write(args_dict["content"])
                else:
                    with open(args_dict["file_path"], "w") as f:
                        f.write(args_dict["content"])
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": f"Wrote to {args_dict['file_path']}"
                    }
                    )
            elif tc.function.name == "Bash":
                import subprocess
                result = subprocess.run(args_dict["command"], shell=True, capture_output=True, text=True)
                result_content = result.stdout if result.returncode == 0 else result.stderr
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": result_content
                    }
                    )


if __name__ == "__main__":
    main()
