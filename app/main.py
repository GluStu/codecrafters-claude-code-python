import argparse
import os
import sys
from openai import OpenAI

API_KEY = os.getenv("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")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")
# is_local = os.environ.get("LOCAL", "false").lower() in ("true", "1", "yes")
# if is_local:
#     model = "z-ai/glm-4.5-air:free"
# else:
model = "anthropic/claude-haiku-4.5"
def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    chat = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": args.p}],
    )

    if not chat.choices or len(chat.choices) == 0:
        raise RuntimeError("no choices in response")

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    # TODO: Uncomment the following line to pass the first stage
    # print(chat.choices[0].message.content)


if __name__ == "__main__":
    main()
