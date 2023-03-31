from engine.engine import ChessEngine
import openai
from flask import Flask, render_template, request, jsonify, session, redirect
from flask_cors import CORS
import uuid
import os
import time

app = Flask(__name__, template_folder=".")
app.secret_key = "862641AD356E286C9B57DB93A9458"
CORS(app)

engine_instances = {}

@app.route("/new-session")
def new_session():
    session_id = str(uuid.uuid4())
    session["session_id"] = session_id
    api_key = session.get("api_key")
    model = session.get("model")
    engine_instances[session_id] = ChessEngine(api_key, model, session_id)
    print(engine_instances)
    return {"session_id": session_id}

@app.route("/delete-session")
def delete_session():
    session_id = session.get("session_id")
    if session_id and session_id in engine_instances:
        del engine_instances[session_id]
        session.clear()
        return {"status": "success"}
    else:
        return {"error": "Invalid session"}
    
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
    status = request.form.get("status")
    pgn_data = request.form.get("pgn")
    san = request.form.get("san")
    result = engine_instance.process_move(move_from, move_to, promotion, status, pgn_data, san)
    return {"move": result}

@app.route("/set-api-key", methods=["POST"])
def set_api_key():
    api_key = request.form.get("api_key")
    model = request.form.get("model")
    session["api_key"] = api_key
    session["model"] = model
    return {"status": "success"}

@app.route("/check-api-key", methods=["POST"])
def check_api_key():
    api_key = request.form.get("api_key")
    openai.api_key = api_key
    try:
        openai.Engine.list()
        return {"status": "success"}
    except openai.error.AuthenticationError:
        return {"status": "failure"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81, debug=True)
