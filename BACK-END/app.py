from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='calendarioeniac',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/datas', methods=['GET'])
def obter_eventos():
    conexao = get_db_connection()
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM dados')
    rows = cursor.fetchall()
    conexao.close()

    eventos = []
    for row in rows:
        eventos.append({
            'id': row['id'],
            'nomeEvento': row['nomeEvento'],
            'dataInicial': row['dataInicial'],
            'dataFinal': row['dataFinal'],
            'descricao': row['descricao']
        })
    return jsonify(eventos)

@app.route('/datas', methods=['POST'])
def add_evento():
    novo_evento = request.get_json()

    nomeEvento = novo_evento.get('nomeEvento')
    dataInicial = novo_evento.get('dataInicial')
    dataFinal = novo_evento.get('dataFinal')
    descricao = novo_evento.get('descricao')

    if not nomeEvento or not dataInicial or not dataFinal:
        return jsonify({'error': 'Faltam campos obrigatórios'}), 400

    conexao = get_db_connection()
    cursor = conexao.cursor()
    cursor.execute(
        'INSERT INTO dados (nomeEvento, dataInicial,dataFinal,descricao) VALUES (%s, %s, %s, %s)',
        (nomeEvento,dataInicial,dataFinal, descricao)
    )
    conexao.commit()
    conexao.close()

    return jsonify({'message': 'Evento inserido com sucesso'}), 201

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)