from engine.engine import engine_instance
#my folder path is called engine/engine.py. I cannot do from engine import engine_instance because of that. what do i need to do instead?
from flask import Flask, render_template, request, jsonify
app = Flask(__name__,  template_folder='.')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    move_from = request.form.get('from')
    move_to = request.form.get('to')
    promotion = request.form.get('promotion')
    result = engine_instance.process_move(move_from, move_to, promotion)
    # Parse the best move from the GPT response
    if '...' in result:
        best_move = result.split("...")[-1].strip().split(".")[0]
    elif 'Best move:' in result:
        best_move = result.split("Best move:")[-1].strip()
    elif 'The PGN of the game now becomes:' in result:
        best_move = result.split("\n")[-3].strip().split(" ")[-1].strip()
    else:
        best_move = result.split("\n")[-1].strip().split(" ")[0]

    # Append the assistant's message to the messages list
    assistant_message = {"role": "assistant", "content": f"PGN of game so far:\n\n{' '.join(engine_instance.pgn_history)}\nBest move: {best_move}"}
    engine_instance.messages.append(assistant_message)

    return {"bestMove": best_move}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)

