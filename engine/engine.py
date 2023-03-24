import openai
from flask_socketio import SocketIO, emit
#import socketio
import time
import threading
import chess
import chess.pgn
import io
import json
import requests
from .config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

class ChessEngine:
    def __init__(self, socketio):
        self.socketio = socketio
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
                    "and then I get to play my move. Do not include the move number'."
                ),
            }
        ]
        self.model = ""

    def set_api_key(self, api_key):
        openai.api_key = api_key

    def set_model(self, model):
        print("model", model)
        self.model = model

    def is_legal_move(self, move):
        try:
            self.board.push_san(move)
            if self.move_count % 2 == 0:  # It's LLM's move
                self.socketio.emit('log_message', f"LLM responded with \"{move}\"")
            return True
        except ValueError:
            if self.move_count % 2 == 0:  # It's LLM's move
                self.socketio.emit('log_message', f"LLM responded with illegal move \"{move}\". Repeat request.")
            return False
        
    #white makes 
    def process_move(self, move_from, move_to, promotion):
        #can remove all prints and than check if each move gets registered 
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
            response = self.get_gpt_response(self.messages)
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
        completion = openai.ChatCompletion.create(
        model=self.model,
        messages=messages
        )
        return completion.choices[0].message["content"].strip()