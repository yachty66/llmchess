# from engine.engine import engine_instance
from engine.engine import ChessEngine
import openai
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import uuid
import os


app = Flask(__name__, template_folder=".")
app.secret_key = "862641AD356E286C9B57DB93A9458"
CORS(app)


# engine_instance = ChessEngine(socketio)
engine_instances = {}


@app.route("/new-session")
def new_session():
    session_id = str(uuid.uuid4())
    session["session_id"] = session_id
    api_key = session.get("api_key")
    model = session.get("model")
    engine_instances[session_id] = ChessEngine(api_key, model)
    # Create a log file for the user
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    with open(os.path.join(log_dir, f"{session_id}.log"), "w") as log_file:
        log_file.write("User session started\n")

    return {"session_id": session_id}


@app.route("/get-logs", methods=["GET"])
def get_logs():
    session_id = session.get("session_id")
    if not session_id:
        return {"error": "Invalid session"}
    log_dir = "logs"
    log_path = os.path.join(log_dir, f"{session_id}.log")
    if os.path.exists(log_path):
        with open(log_path, "r") as log_file:
            logs = log_file.read()
        return {"logs": logs}
    else:
        return {"error": "Log file not found"}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/move", methods=["POST"])
def move():
    session_id = session.get("session_id")
    if not session_id or session_id not in engine_instances:
        return {"error": "Invalid session"}
    engine_instance = engine_instances[session_id]
    move_from = request.form.get("from")
    move_to = request.form.get("to")
    promotion = request.form.get("promotion")
    result = engine_instance.process_move(move_from, move_to, promotion)
    return {"move": result}


"""@app.route('/move', methods=['POST'])
def move():
    move_from = request.form.get('from')
    move_to = request.form.get('to')
    promotion = request.form.get('promotion')
    result = engine_instance.process_move(move_from, move_to, promotion)
    return {"move": result}"""

"""@app.route('/set-api-key', methods=['POST'])
def set_api_key():
    api_key = request.form.get('api_key')
    model = request.form.get('model')
    engine_instance.set_api_key(api_key)
    engine_instance.set_model(model)
    return {"status": "success"}"""


@app.route("/set-api-key", methods=["POST"])
def set_api_key():
    print("set api key")
    api_key = request.form.get("api_key")
    model = request.form.get("model")
    session["api_key"] = api_key
    print(session["api_key"])
    session["model"] = model
    print(session["model"])
    return {"status": "success"}


@app.route("/check-api-key", methods=["POST"])
def check_api_key():
    print("check api key")
    api_key = request.form.get("api_key")
    openai.api_key = api_key
    try:
        # Test the API key with a simple request
        openai.Engine.list()
        print("success")
        return {"status": "success"}
    except openai.error.AuthenticationError:
        print("failure")
        return {"status": "failure"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81, debug=True)
