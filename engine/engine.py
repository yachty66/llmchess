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

class ChessEngine:
    def __init__(self, socketio, api_key=None, model=None):
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
        self.game_over = False
        self.api_key = api_key
        self.model = model

    def set_api_key(self):
        openai.api_key = self.api_key

    def set_model(self):
        self.model = self.model

    def is_legal_move(self, move):
        #check here if game is over and in this case send log to the frontend.
        try:
            self.board.push_san(move)
            self.socketio.emit('log_message', f"LLM responded with \"{move}\"")
            if self.board.is_game_over():
                self.socketio.emit('log_message', 'Game over')
                self.game_over = False
            return True
        except ValueError:
            self.socketio.emit('log_message', f"LLM responded with illegal move \"{move}\". Repeat request.")
            return False
        
    #white makes 
    def process_move(self, move_from, move_to, promotion):
        if self.game_over:
            return 
        self.move_count += 1
        if self.move_count == 2:
            # TODO make dynamically
            self.board.push_san("e4")
            response = self.get_gpt_response(self.messages)
            move = response.split("Best move:")[-1].strip().split()[0]
            while True:
                if self.is_legal_move(move):
                    self.messages.append({"role": "assistant", "content": response})
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
        #url = "https://api.openai.com/v1/chat/completions"
        completion = openai.ChatCompletion.create(
        model=self.model,
        messages=messages
        )
        return completion.choices[0].message["content"].strip()