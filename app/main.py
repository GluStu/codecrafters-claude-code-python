import argparse
import os
import sys
from openai import OpenAI
import json


API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")
model = "anthropic/claude-haiku-4.5"
def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    message_history = [{"role": "user", "content": args.p}]

    while True:

        chat = client.chat.completions.create(
            model=model,
            messages=message_history,
            tools=[{
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
                }]
        )

        if not chat.choices or len(chat.choices) == 0:
            raise RuntimeError("no choices in response")
        print("Logs from your program will appear here!", file=sys.stderr)

        message = chat.choices[0].message
        message_history.append(message)

        if not message.tool_calls:
            print(message.content.strip())
            break

        for tool_call in message.tool_calls or []:
            args = json.loads(tool_call.function.arguments)

            if tool_call.function.name == "Read":
                with open(args["file_path"]) as f:
                    content = f.read()
                    
                    message_history.append(
                        {"role": "tool",
                         "tool_call_id": tool_call.id,
                         "content": content
                        })
        continue
    

if __name__ == "__main__":
    main()
