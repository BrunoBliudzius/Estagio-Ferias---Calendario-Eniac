from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app, supports_credentials=True)

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='calendarioeniac',
        cursorclass=pymysql.cursors.DictCursor
    )

# GET - Obter todos os eventos
@app.route('/datas', methods=['GET'])
def obter_eventos():
    conexao = get_db_connection()
    cursor = conexao.cursor()
    try:
        cursor.execute('SELECT * FROM dados')
        rows = cursor.fetchall()
        eventos = []
        for row in rows:
            eventos.append({
                'id': row['id'],
                'nomeEvento': row['nomeEvento'],
                'dataInicial': row['dataInicial'],
                'dataFinal': row['dataFinal'],
                'descricao': row['descricao'],
                'eventColor': row['eventColor']
            })
        return jsonify(eventos)
    finally:
        cursor.close()
        conexao.close()

# POST - Cadastrar novo evento
@app.route('/datas', methods=['POST'])
def add_evento():
    novo_evento = request.get_json()
    nomeEvento = novo_evento.get('nomeEvento')
    dataInicial = novo_evento.get('dataInicial')
    dataFinal = novo_evento.get('dataFinal')
    descricao = novo_evento.get('descricao', '')
    eventColor = novo_evento.get('eventColor', '#3788d8')

    if not nomeEvento or not dataInicial or not dataFinal:
        return jsonify({'error': 'Faltam campos obrigatórios'}), 400

    conexao = get_db_connection()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            'INSERT INTO dados (nomeEvento, dataInicial, dataFinal, descricao, eventColor) VALUES (%s, %s, %s, %s, %s)',
            (nomeEvento, dataInicial, dataFinal, descricao, eventColor)
        )
        conexao.commit()
        return jsonify({'message': 'Evento inserido com sucesso'}), 201
    finally:
        cursor.close()
        conexao.close()

# PUT - Atualizar evento existente
@app.route('/datas/<int:id>', methods=['PUT'])
def atualizar_evento(id):
    dados = request.get_json()
    nomeEvento = dados.get('nomeEvento')
    dataInicial = dados.get('dataInicial')
    dataFinal = dados.get('dataFinal')
    descricao = dados.get('descricao', '')
    eventColor = dados.get('eventColor')  # <- Agora é usado corretamente

    if not nomeEvento or not dataInicial or not dataFinal:
        return jsonify({'erro': 'Campos obrigatórios faltando'}), 400

    conexao = get_db_connection()
    cursor = conexao.cursor()
    try:
        sql = """
            UPDATE dados
            SET nomeEvento = %s,
                dataInicial = %s,
                dataFinal = %s,
                descricao = %s,
                eventColor = %s
            WHERE id = %s
        """
        valores = (nomeEvento, dataInicial, dataFinal, descricao, eventColor, id)
        cursor.execute(sql, valores)
        conexao.commit()

        if cursor.rowcount == 0:
            return jsonify({'erro': 'Evento não encontrado'}), 404

        return jsonify({'mensagem': 'Evento atualizado com sucesso'})
    finally:
        cursor.close()
        conexao.close()

# DELETE - Excluir evento
@app.route('/datas/<int:id>', methods=['DELETE'])
def deletar_evento(id):
    conexao = get_db_connection()
    cursor = conexao.cursor()
    try:
        sql = "DELETE FROM dados WHERE id = %s"
        cursor.execute(sql, (id,))
        conexao.commit()

        if cursor.rowcount == 0:
            return jsonify({'erro': 'Evento não encontrado'}), 404

        return jsonify({'mensagem': 'Evento excluído com sucesso'})
    finally:
        cursor.close()
        conexao.close()

# GET - Filtro por nome do evento
@app.route('/datasFiltro', methods=['GET'])
def obter_evento_por_nome():
    nome_evento = request.args.get('nomeEvento')
    if not nome_evento:
        return jsonify({'erro': 'Parâmetro nomeEvento é obrigatório'}), 400

    conexao = get_db_connection()
    cursor = conexao.cursor()
    try:
        sql = "SELECT * FROM dados WHERE nomeEvento LIKE %s"
        cursor.execute(sql, ('%' + nome_evento + '%',))
        rows = cursor.fetchall()

        eventos = []
        for row in rows:
            eventos.append({
                'id': row['id'],
                'nomeEvento': row['nomeEvento'],
                'dataInicial': row['dataInicial'],
                'dataFinal': row['dataFinal'],
                'descricao': row['descricao'],
                'eventColor': row['eventColor']  # incluir cor aqui também
            })

        return jsonify(eventos)
    finally:
        cursor.close()
        conexao.close()

# Roda o servidor
if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)
