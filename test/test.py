
#import your_chess_engine
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)


@app.route('/')
def index():
    return "hey"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)

