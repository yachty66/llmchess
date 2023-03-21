from engine.engine import engine_instance
#my folder path is called engine/engine.py. I cannot do from engine import engine_instance because of that. what do i need to do instead?
from flask import Flask, render_template, request, jsonify
app = Flask(__name__,  template_folder='.')


@app.route('/')
def index():
    return render_template('index.html')

#ive created a post request "Hello world" from my js code. how can i send something back like "hello" 
@app.route('/hello', methods=["GET", 'POST'])
def hello():
    return "hellohello"

@app.route('/best_move', methods=["GET", 'POST'])
def best_move():
    fen = request.form.get('fen')
    #best_move = engine.get_best_move(fen)
    return jsonify(move=best_move)

@app.route('/move', methods=['POST'])
def move():
    move_from = request.form.get('from')
    move_to = request.form.get('to')
    promotion = request.form.get('promotion')
    result = engine_instance.process_move(move_from, move_to, promotion)
    if engine_instance.move_count == 1:
        # Parse the best move from the GPT response
        best_move = result.split("Best move:")[-1].strip()
        return {"bestMove": best_move}
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)

