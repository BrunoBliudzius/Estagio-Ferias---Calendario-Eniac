from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

datas = [
    {
        "id": 1,
        "title": "Aula de futebol",
        "start": "2025-07-07",
        
    },
    {
        "id": 2,
        "title": "Aula de judo",
        "start": "2025-07-10",
        
    },
    {
        "id": 3,
        "title": "Aula de dança",
        "start": "2025-07-08",
    }
]

@app.route('/datas', methods=['GET'])
def obter_eventos():
    return jsonify(datas)
app.run(port=5000, host='localhost', debug=True)