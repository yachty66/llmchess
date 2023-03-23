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
    '''pgn = request.form.get('pgn')
    result = engine_instance.process_move_pgn(pgn)'''
    return {"move": result}
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)

