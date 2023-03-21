import openai
import json
import requests
from .config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

class ChessEngine:
    def __init__(self):
        self.move_count = 0

    def process_move(self, move_from, move_to, promotion):
        self.move_count += 1
        pgn = f"{self.move_count}. {move_from}{move_to}"
        if self.move_count == 1:
            #1.e4 is currently hardcoded but need to be adjusted depending on the first move
            prompt = f"We are playing a chess game. At every turn, repeat all the moves that have already been made. Find the best response for Black. I'm White and the game starts with {pgn}\n\nPGN of game so far: {pgn}\n\nBest move:"
            gpt_response = self.get_gpt_response(prompt)

            return gpt_response

        # Add any additional logic for processing moves here
        # ...

        return "Move processed"
    
    def get_gpt_response(self, prompt):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + OPENAI_API_KEY,
        }
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_json = response.json()
        print(response_json)
        return response_json['choices'][0]['message']['content'].strip()


engine_instance = ChessEngine()


'''
We are playing a chess game. At every turn, repeat all the moves that have already been made. Find the best response for Black. I'm White and the game starts with 1.e4

So, to be clear, your output format should always be: 

PGN of game so far: ... 

Best move: ... 

and then I get to play my move.
'''

# else send string in fen

#check if move which comes back is legal. if not legal print no legal move and repreat prev request. always print full response 
