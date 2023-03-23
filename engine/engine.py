import openai
import chess
import chess.pgn
import io
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

    #create a method which checks if the move is legal
    def is_legal_move(self, move):
        try:
            print(self.board)
            self.board.push_san(move)
            return True
        except ValueError:
            return False

    def process_move(self, move_from, move_to, promotion):
        print(self.move_count)
        self.move_count += 1
        if self.move_count == 2:
            # TODO make dynamically
            self.board.push_san("e4")
            response = self.get_gpt_response(self.messages)
            self.messages.append({"role": "assistant", "content": response})
            move = response.split("Best move:")[-1].strip().split()[0]
            while True:
                is_legal = self.is_legal_move(move)
                if is_legal:
                    break
                else:
                    response = self.get_gpt_response(self.messages)
                    move = response.split("Best move:")[-1].strip().split()[0]
            return self.board.uci(chess.Move.from_uci(self.board.move_stack[1].uci()))
        """
        - [x] make beginning always working
        - [x] start loop 
        - [x] convert move to san
        - [x] make request with new move
        - [x] check if move is valid  
        - [x] if valid return move in uci and add to board
        - [x] if not print something and repeat
        - [ ] find out why stop with responding
        """
        san_move = self.board.san(chess.Move.from_uci(move_from + move_to))
        self.messages.append({"role": "user", "content": f"{san_move}"})
        self.board.push_san(san_move)
        while True:
            response = self.get_gpt_response(self.messages)
            print("20*-")
            print(response)
            #get move from response
            move = response.split("Best move:")[-1].strip().split()[0]
            #validate move
            #first need to add move to board
            if self.is_legal_move(move):
                self.messages.append({"role": "assistant", "content": response})
                uci_move = self.board.peek().uci()
                return uci_move
            else:
                print("not a legal move", move)
                continue

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
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_json = response.json()
        return response_json["choices"][0]["message"]["content"].strip()
    


engine_instance = ChessEngine()
