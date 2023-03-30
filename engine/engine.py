import openai
import chess
import chess.pgn
import re

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
                    "and then I get to play my move. Do not include the move number."
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
        move_pattern = re.compile(r'Best move:.*?\b(?:\d+\.\.\.)?([a-h][1-8][QNRB]?|O-O(?:-O)?)\b')
        try:
            match = move_pattern.search(response)
            if match:
                return match.group(1)
            else:
                return "Model response did not contain a move"
        except Exception as e:
            print(f"An error occurred while extracting the move: {e}")
            return "Model response did not contain a move"

    def is_legal_move(self, move):
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
            return False

    def update_first_move_message(self, first_move):
        self.messages[0]["content"] = self.messages[0]["content"].format(
            first_move=first_move
        )

    def get_next_log(self):
        if len(self.logs) > 0:
            return self.logs.pop(0)
        else:
            return None

    def process_move(self, move_from, move_to, promotion):
        if self.game_over:
            return
        self.move_count += 1
        if self.move_count == 2:
            uci_move = move_from + move_to
            san_move = self.board.san(chess.Move.from_uci(uci_move))
            self.board.push_san(san_move)
            self.update_first_move_message(san_move)
            response = self.get_gpt_response(self.messages)
            move = self.extract_move(response)
            while True:
                if self.is_legal_move(move):
                    self.messages.append({"role": "assistant", "content": response})
                    break
                else:
                    response = self.get_gpt_response(self.messages)
                    move = self.extract_move(response)
            return self.board.uci(chess.Move.from_uci(self.board.move_stack[1].uci()))
        san_move = self.board.san(chess.Move.from_uci(move_from + move_to))
        self.messages.append({"role": "user", "content": f"{san_move}"})
        self.board.push_san(san_move)
        while True:
            response = self.get_gpt_response(self.messages)
            move = self.extract_move(response)
            if self.is_legal_move(move):
                self.messages.append({"role": "assistant", "content": response})
                uci_move = self.board.peek().uci()
                return uci_move
            else:
                print("not a legal move", move)
                continue

    def get_gpt_response(self, messages):
        completion = openai.ChatCompletion.create(model=self.model, messages=messages)
        return completion.choices[0].message["content"].strip()
