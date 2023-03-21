
#import your_chess_engine
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
    return jsonify(move="e2e4")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)

