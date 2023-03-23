#from engine.engine import engine_instance
from engine.engine import ChessEngine
import openai
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
app = Flask(__name__,  template_folder='.')
socketio = SocketIO(app, cors_allowed_origins="*")

engine_instance = ChessEngine(socketio)  

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

@app.route('/set-api-key', methods=['POST'])
def set_api_key():
    api_key = request.form.get('api_key')
    engine_instance.set_api_key(api_key)
    return {"status": "success"}

@app.route('/check-api-key', methods=['POST'])
def check_api_key():
    api_key = request.form.get('api_key')
    openai.api_key = api_key
    try:
        # Test the API key with a simple request
        openai.Engine.list()
        return {"status": "success"}
    except openai.error.AuthenticationError:
        return {"status": "failure"}

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('log_message')
def handle_log_message(message):
    print('Received message:', message)
    emit('log_message', message, broadcast=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)

