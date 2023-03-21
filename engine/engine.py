import openai
import json
import requests
from .config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

class ChessEngine:
    def __init__(self):
        self.move_count = 0
        self.pgn_history = []

    def process_move(self, move_from, move_to, promotion):
        self.move_count += 1
        pgn = f"{move_from}{move_to}"
        self.pgn_history.append(pgn)

        # Join the PGN history with alternating numbers and moves
        pgn_string = " ".join(
            f"{i // 2 + 1}. {move}" if i % 2 == 0 else move
            for i, move in enumerate(self.pgn_history)
        )

        prompt = f"We are playing a chess game. At every turn, repeat all the moves that have already been made. Find the best response for {'Black' if self.move_count % 2 == 1 else 'White'}. I'm {'White' if self.move_count % 2 == 0 else 'Black'} and the game starts with {self.pgn_history[0]}\n\nPGN of game so far: {pgn_string}\n\nBest move:"
        gpt_response = self.get_gpt_response(prompt)

        return gpt_response
    
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
