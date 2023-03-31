import openai
import chess
import chess.pgn
import io


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
        response = response.replace("...", "")
        response = response.replace("1.", "")
        response = response.replace(".", "")
        response = response.replace(" ", "")
        #in case response is wrong shorten
        response = response[:10]
        return response

    def update_first_move_message(self, first_move):
        self.messages[0]["content"] = self.messages[0]["content"].format(
            first_move=first_move
        )

    def process_move(self, move_from, move_to, promotion, status, pgn, san):
        pgn_game = chess.pgn.read_game(io.StringIO(pgn))
        self.move_count += 1
        if status == "repeat":
            self.messages.pop()
            response = self.get_gpt_response(self.messages)
            self.messages.append({"role": "assistant", "content": response})
            extracted_move = self.extract_move(response)
            return extracted_move
        if self.move_count == 2:
            root_node = pgn_game.game()
            first_move = root_node.variations[0].move
            initial_board = chess.Board()
            san_move = initial_board.san(first_move)
            self.update_first_move_message(san_move)
            response = self.get_gpt_response(self.messages)
            self.messages.append({"role": "assistant", "content": response})
            extracted_move = self.extract_move(response)
            return extracted_move
        san_move = san
        self.messages.append({"role": "user", "content": f"{san_move}"})
        response = self.get_gpt_response(self.messages)
        self.messages.append({"role": "assistant", "content": response})
        extracted_move = self.extract_move(response)
        return extracted_move

    def get_gpt_response(self, messages):
        completion = openai.ChatCompletion.create(model=self.model, messages=messages)
        return completion.choices[0].message["content"].strip()
