#from engine.engine import engine_instance
from engine.engine import ChessEngine
import openai
from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import uuid


app = Flask(__name__,  template_folder='.')
app.secret_key = '862641AD356E286C9B57DB93A9458'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

#engine_instance = ChessEngine(socketio)  
engine_instances = {}

@app.route('/new-session')
def new_session():
    session_id = str(uuid.uuid4())
    session['session_id'] = session_id
    api_key = session.get('api_key')
    model = session.get('model')
    engine_instances[session_id] = ChessEngine(socketio, api_key, model)
    return {'session_id': session_id}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    session_id = session.get('session_id')
    if not session_id or session_id not in engine_instances:
        return {"error": "Invalid session"}
    engine_instance = engine_instances[session_id]
    move_from = request.form.get('from')
    move_to = request.form.get('to')
    promotion = request.form.get('promotion')
    result = engine_instance.process_move(move_from, move_to, promotion)
    return {"move": result}

'''@app.route('/move', methods=['POST'])
def move():
    move_from = request.form.get('from')
    move_to = request.form.get('to')
    promotion = request.form.get('promotion')
    result = engine_instance.process_move(move_from, move_to, promotion)
    return {"move": result}'''

'''@app.route('/set-api-key', methods=['POST'])
def set_api_key():
    api_key = request.form.get('api_key')
    model = request.form.get('model')
    engine_instance.set_api_key(api_key)
    engine_instance.set_model(model)
    return {"status": "success"}'''

@app.route('/set-api-key', methods=['POST'])
def set_api_key():
    api_key = request.form.get('api_key')
    model = request.form.get('model')
    session['api_key'] = api_key
    session['model'] = model
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

