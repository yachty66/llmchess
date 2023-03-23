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
        san_move = self.board.san(chess.Move.from_uci(move_from + move_to))
        self.messages.append({"role": "user", "content": f"{san_move}"})
        self.board.push_san(san_move)
        while True:
            print("next round")
            response = self.get_gpt_response(self.messages)
            print("response",response)
            move = response.split("Best move:")[-1].strip().split()[0]
            if self.is_legal_move(move):
                self.messages.append({"role": "assistant", "content": response})
                uci_move = self.board.peek().uci()
                return uci_move
            else:
                print("not a legal move", move)
                continue

    def get_gpt_response(self, messages):
        url = "https://api.openai.com/v1/chat/completions"
        print("messages", messages)

        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=messages
        )
        return completion.choices[0].message["content"].strip()
    
engine_instance = ChessEngine()
