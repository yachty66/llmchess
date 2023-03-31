from engine.engine import ChessEngine
import logging
import openai
from flask import Flask, render_template, request, jsonify, session, redirect
from flask_session import Session
from flask_cors import CORS
from flask.sessions import SecureCookieSessionInterface
import uuid
from datetime import datetime
from datetime import timedelta

app = Flask(__name__, template_folder=".")
app.secret_key = "sf43d5f4s394jfe2dm903"
app.logger.setLevel(logging.DEBUG)
CORS(app)

engine_instances = {}

@app.route("/new-session")
def new_session():
    session_id = str(uuid.uuid4())
    session["session_id"] = session_id
    api_key = session.get("api_key")
    model = session.get("model")
    engine_instances[session_id] = ChessEngine(api_key, model, session_id)
    print(f"New session created: {session_id}, session content: {dict(session)}, engine_instances: {engine_instances}")
    #print("New session created:", session_id)
    return {"session_id": session_id}

@app.route("/delete-session")
def delete_session():
    session_id = session.get("session_id")
    if session_id in engine_instances:
        del engine_instances[session_id]
        session.clear()
        return {"status": "success"}
    else:
        print("invalid session in delete-session")
        return {"error": "Invalid session"}
    
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    print(f"Before move, session content: {dict(session)}, engine_instances: {engine_instances}")
    session_id = session.get("session_id")
    if not session_id or session_id not in engine_instances:
        print(f"Invalid session in move: {session_id}")
        return {"error": "Invalid session"}
    engine_instance = engine_instances[session_id]
    move_from = request.form.get("from")
    move_to = request.form.get("to")
    promotion = request.form.get("promotion")
    status = request.form.get("status")
    pgn_data = request.form.get("pgn")
    san = request.form.get("san")
    result = engine_instance.process_move(move_from, move_to, promotion, status, pgn_data, san)
    print(f"After move, session content: {dict(session)}, engine_instances: {engine_instances}")
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

