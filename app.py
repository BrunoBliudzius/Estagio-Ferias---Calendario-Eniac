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
            'descricao': row['descricao'],
            'dataCalendario': row['dataCalendario']
        })
    return jsonify(eventos)

@app.route('/datas', methods=['POST'])
def add_evento():
    novo_evento = request.get_json()

    descricao = novo_evento.get('descricao')
    data_calendario = novo_evento.get('dataCalendario')

    if not descricao or not data_calendario:
        return jsonify({'error': 'Faltam campos obrigatórios'}), 400

    conexao = get_db_connection()
    cursor = conexao.cursor()
    cursor.execute(
        'INSERT INTO dados (descricao, dataCalendario) VALUES (%s, %s)',
        (descricao, data_calendario)
    )
    conexao.commit()
    conexao.close()

    return jsonify({'message': 'Evento inserido com sucesso'}), 201

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)
