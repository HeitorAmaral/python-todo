from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def ping():
    return jsonify({'message': 'The backend is working!'}), 200


if __name__ == '__main__':
    app.run()
