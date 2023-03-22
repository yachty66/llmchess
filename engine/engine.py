import openai
import chess
import json
import requests
from .config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


class ChessEngine:
    def __init__(self):
        self.move_count = 1
        self.board = chess.Board()
        self.messages = [
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

    def process_move(self, move_from, move_to, promotion):
        self.move_count += 1
        if self.move_count == 2:
            response = self.get_gpt_response(self.messages)
            self.messages.append({"role": "assistant", "content": response})
            #TODO can be checked if legal move 
            move = response.split("Best move:")[-1].strip().split()[0]
            # TODO make dynamically
            self.board.push_san("e4")
            self.board.push_san(move)
            return self.board.uci(chess.Move.from_uci(self.board.move_stack[1].uci()))


    def get_gpt_response(self, messages):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + OPENAI_API_KEY,
        }
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": 0.7,
        }
        print("messages: ", messages)
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_json = response.json()
        return response_json["choices"][0]["message"]["content"].strip()


engine_instance = ChessEngine()
