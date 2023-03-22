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

    def convert_to_pgn(self, move_from, move_to, promotion):
        uci_move = move_from + move_to
        move_obj = chess.Move.from_uci(uci_move)
        if promotion:
            move_obj = chess.Move(
                move_obj.from_square,
                move_obj.to_square,
                promotion=chess.Piece.from_symbol(promotion),
            )
        self.board.push(move_obj)

        game = chess.pgn.Game()
        node = game.add_variation(move_obj)

        pgn_string = io.StringIO()
        print("pgn string", pgn_string.getvalue())
        game.accept(chess.pgn.StringExporter(pgn_string))
        pgn_string = pgn_string.getvalue()
        return pgn_string

    def process_move(self, move_from, move_to, promotion):
        self.move_count += 1
        if self.move_count == 2:
            response = self.get_gpt_response(self.messages)
            self.messages.append({"role": "assistant", "content": response})
            # TODO can be checked if legal move
            move = response.split("Best move:")[-1].strip().split()[0]
            # TODO make dynamically
            self.board.push_san("e4")
            print("move", move)
            self.board.push_san(move)
            return self.board.uci(chess.Move.from_uci(self.board.move_stack[1].uci()))
        """
        - [x] start loop 
        - [ ] convert move to pgn 
        - [ ] make request with new move
        - [ ] check if move is valid  
        - [ ] if valid return move in uci and add to board
        - [ ] if not print something and repeat
        """
        while True:
            # what happens is that a wrong move is suggested and this is why i cannot do a request
            # no the move is for sure a valid move because the move is coming from the frontend.

            #is that legit what i am doing here? if first move add first to moves to board. is the baord alright?
            #okay second move is on the board but than error:

            #the second move is not on the board 
            print(self.board)
            pgn = self.convert_to_pgn(move_from, move_to, promotion)
            print(pgn)
            break

            # move = chess.Move.from_uci(move_from + move_to)
            # print(move)
            # self.messages.append({"role": "user", "content": f"{move_from} {move_to} {promotion}"})

    def process_move_pgn(self, pgn):
        # Load the provided PGN into a chess.pgn.Game object
        game = chess.pgn.read_game(io.StringIO(pgn))
        print("game", game)
        # Find the latest move in the game
        latest_move = None
        node = game.end()
        if node.move:
            latest_move = node.move

        if latest_move:
            self.board.push(latest_move)


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
