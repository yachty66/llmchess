from engine.engine import ChessEngine
import openai
from flask import Flask, render_template, request, session
from flask_cors import CORS
import uuid
from google.cloud import datastore
import pickle

datastore_client = datastore.Client()

def store_instance(session_id, engine_instance):
    serialized_instance = pickle.dumps(engine_instance)

    key = datastore_client.key('ChessEngine', session_id)
    entity = datastore.Entity(key=key, exclude_from_indexes=('instance',))
    entity.update({
        'instance': serialized_instance
    })

    datastore_client.put(entity)

def get_instance(session_id):
    key = datastore_client.key('ChessEngine', session_id)
    entity = datastore_client.get(key)
    if entity is None:
        return None
    return pickle.loads(entity['instance'])

def delete_instance(session_id):
    key = datastore_client.key('ChessEngine', session_id)
    datastore_client.delete(key)


app = Flask(__name__, template_folder=".")
app.secret_key = "sf43d5f4s394jfe2dm903"
CORS(app)

@app.route("/new-session")
def new_session():
    session_id = str(uuid.uuid4())
    session["session_id"] = session_id
    api_key = session.get("api_key")
    model = session.get("model")
    store_instance(session_id, ChessEngine(api_key, model, session_id))
    print(f"New session created: {session_id}, session content: {dict(session)}")
    return {"session_id": session_id}

@app.route("/delete-session")
def delete_session():
    session_id = session.get("session_id")
    if get_instance(session_id) is not None:
        delete_instance(session_id)
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
    print(f"Before move, session content: {dict(session)}")
    session_id = session.get("session_id")
    engine_instance = get_instance(session_id)
    if not session_id or engine_instance is None:
        print(f"Invalid session in move: {session_id}")
        return {"error": "Invalid session"}
    move_from = request.form.get("from")
    move_to = request.form.get("to")
    promotion = request.form.get("promotion")
    status = request.form.get("status")
    pgn_data = request.form.get("pgn")
    san = request.form.get("san")
    result = engine_instance.process_move(move_from, move_to, promotion, status, pgn_data, san)
    store_instance(session_id, engine_instance)
    print(f"New session created: {session_id}, session content: {dict(session)}")
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

