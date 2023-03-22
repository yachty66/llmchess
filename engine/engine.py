import openai
import chess 
import json
import requests
from .config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

class ChessEngine:
    def __init__(self):
        self.move_count = 0
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
        initial_response = self.get_gpt_response(self.messages)

        # Extract the first move from the initial response
        #TODO make dynamically
        first_move = "e4"
        self.board.push_san(first_move)
        second_move = initial_response.split("Best move:")[-1].strip().split()[0]
        self.board.push_san(second_move)
        self.messages.append({"role": "assistant", "content": initial_response})



    def process_move(self, move_from, move_to, promotion):
        '''
        move comes inside.
        1. make move from the initial response 
        1. convert incoming move to png
        '''
        #if len of board two return second move 
        if len(self.board.move_stack) == 2:
            #return second move in uci
            print(self.board.uci(chess.Move.from_uci(self.board.move_stack[1].uci())))
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
        return response_json['choices'][0]['message']['content'].strip()



engine_instance = ChessEngine()

