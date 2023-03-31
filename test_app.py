from flask import Flask, session, request, jsonify

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/set-api-key', methods=['POST'])
def set_api_key():
    api_key = request.form.get('api_key')
    session['api_key'] = api_key
    return jsonify(status='success')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)


