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

class PermanentSessionLifetimeInterface(SecureCookieSessionInterface):
    def get_expiration_time(self, app, session):
        return datetime.utcnow() + app.permanent_session_lifetime

app = Flask(__name__, template_folder=".")
app.secret_key = "sf43d5f4s394jfe2dm903"
app.permanent_session_lifetime = timedelta(days=30)
app.session_interface = PermanentSessionLifetimeInterface()
CORS(app)

engine_instances = {}

@app.before_request
def make_session_permanent():
    session.permanent = True

@app.route("/new-session")
def new_session():
    session_id = str(uuid.uuid4())
    session["session_id"] = session_id
    api_key = session.get("api_key")
    model = session.get("model")
    engine_instances[session_id] = ChessEngine(api_key, model, session_id)
    logging.debug(f"New session created: {session_id}")
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

