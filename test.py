import openai
openai.api_key = "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"

messages = [
            {
                "role": "system",
                "content": (
                    "We are playing a chess game. At every turn, repeat all the moves that have already been made."
                    "Find the best response for Black. I'm White and the game starts with 1.e4\n\n"
                    "So, to be clear, your output format should always be:\n\n"
                    "PGN of game so far: ...\n\n"
                    "Best move: ...\n\n"
                    "and then I get to play my move."
                ),
            }
        ]

url = "https://api.openai.com/v1/chat/completions"
completion = openai.ChatCompletion.create(
model="gpt-4",
messages=messages
)
print(completion.choices[0].message["content"].strip())