import openai
import re
import os
import time
import threading
import chess
import chess.pgn
import io
import json
import requests


class ChessEngine:
    def __init__(self, api_key=None, model=None, session_id=None):
        self.move_count = 1
        self.board = chess.Board()
        self.messages = [
            {
                "role": "system",
                "content": (
                    "We are playing a chess game. At every turn, repeat all the moves that have already been made."
                    "Find the best response for Black. I'm White and the game starts with 1.{first_move}\n\n"
                    "So, to be clear, your output format should always be:\n\n"
                    "PGN of game so far: ...\n\n"
                    "Best move: ...\n\n"
                    "and then I get to play my move. Do not include the move number'."
                ),
            }
        ]
        self.logs = []
        self.game_over = False
        self.api_key = api_key
        self.model = model
        self.session_id = session_id

    def set_api_key(self):
        openai.api_key = self.api_key

    def set_model(self):
        self.model = self.model

    def extract_move(self, response):
        response = response.split("Best move:")[1]
        response = response.replace("...","")
        response = response.replace("1.","")
        response = response.replace(".","")
        response = response.replace(" ","")
        return response

    '''def is_legal_move(self, move):
        try:
            self.board.push_san(move)
            log_message = f'LLM responded with "{move}"'
            self.logs.append(log_message)
            if self.board.is_game_over():
                log_message = "Game over"
                self.logs.append(log_message)
                self.game_over = False
            return True
        except ValueError:
            log_message = f'LLM responded with illegal move "{move}". Repeat request.'
            self.logs.append(log_message)
            return False'''

    def update_first_move_message(self, first_move):
        self.messages[0]["content"] = self.messages[0]["content"].format(
            first_move=first_move
        )

    def get_next_log(self):
        if len(self.logs) > 0:
            return self.logs.pop(0)
        else:
            return None

    #i.e. what we can do is we can 
    def process_move(self, move_from, move_to, promotion, status, pgn, san):
        pgn_game = chess.pgn.read_game(io.StringIO(pgn))
        #pgn_board.set_epd(pgn_game.end().board().epd())
        self.move_count += 1
        if status == "repeat":
            self.messages.pop()
            response = self.get_gpt_response(self.messages)
            self.messages.append({"role": "assistant", "content": response})
            extracted_move = self.extract_move(response)
            return extracted_move
        #i can send from the frontedn some information if it is the opponents first move and based on that i can 
        if self.move_count == 2:
            root_node = pgn_game.game()
            first_move = root_node.variations[0].move
            initial_board = chess.Board()
            san_move = initial_board.san(first_move)
            #san_move = pgn_board.san(first_move)
            self.update_first_move_message(san_move)
            response = self.get_gpt_response(self.messages)
            self.messages.append({"role": "assistant", "content": response})
            extracted_move = self.extract_move(response)
            #this needs to be send to the frontend again
            return extracted_move
        san_move = san
        self.messages.append({"role": "user", "content": f"{san_move}"})
        response = self.get_gpt_response(self.messages)
        self.messages.append({"role": "assistant", "content": response})
        extracted_move = self.extract_move(response)
        return extracted_move

    '''def process_move(self, move_from, move_to, promotion):
        #this method is called from the server
        if self.game_over:
            return
        self.move_count += 1
        if self.move_count == 2:
            uci_move = move_from + move_to
            san_move = self.board.san(chess.Move.from_uci(uci_move))
            self.board.push_san(san_move)
            self.update_first_move_message(san_move)
            response = self.get_gpt_response(self.messages)
            while True:
                try:
                    move = response.split("Best move:")[-1].strip().split()[0]
                    break
                except:
                    continue
            while True:
                if self.is_legal_move(move):
                    self.messages.append({"role": "assistant", "content": response})
                    break
                else:
                    response = self.get_gpt_response(self.messages)
                    while True:
                        try:
                            move = response.split("Best move:")[-1].strip().split()[0]
                            break
                        except:
                            continue
                    move = response.split("Best move:")[-1].strip().split()[0]
            return self.board.uci(chess.Move.from_uci(self.board.move_stack[1].uci()))
        san_move = self.board.san(chess.Move.from_uci(move_from + move_to))
        self.messages.append({"role": "user", "content": f"{san_move}"})
        self.board.push_san(san_move)
        while True:
            response = self.get_gpt_response(self.messages)
            while True:
                try:
                    move = response.split("Best move:")[-1].strip().split()[0]
                    break
                except:
                    continue
            if self.is_legal_move(move):
                self.messages.append({"role": "assistant", "content": response})
                uci_move = self.board.peek().uci()
                return uci_move
            else:
                print("not a legal move", move)
                continue'''

    def get_gpt_response(self, messages):
        completion = openai.ChatCompletion.create(model=self.model, messages=messages)
        return completion.choices[0].message["content"].strip()
