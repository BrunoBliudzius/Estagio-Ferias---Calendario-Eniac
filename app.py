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
        
    }
]

@app.route('/datas')
def obter_eventos():
    return jsonify(datas)
app.run(port=5000, host='localhost', debug=True)