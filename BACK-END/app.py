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
            'descricao': row.get('descricao'), # Use .get() para campos opcionais
            'eventColor': row.get('eventColor', '#054161') # Obtém a cor ou usa a padrão
        })
    return jsonify(eventos)


@app.route('/datas', methods=['POST'])
def add_evento():
    novo_evento = request.get_json()


    nomeEvento = novo_evento.get('nomeEvento')
    dataInicial = novo_evento.get('dataInicial')
    dataFinal = novo_evento.get('dataFinal')
    descricao = novo_evento.get('descricao')
    eventColor = novo_evento.get('eventColor', '#054161') # Obtém a cor ou usa a padrão


    if not nomeEvento or not dataInicial or not dataFinal:
        return jsonify({'error': 'Faltam campos obrigatórios'}), 400


    conexao = get_db_connection()
    cursor = conexao.cursor()
    cursor.execute(
        'INSERT INTO dados (nomeEvento, dataInicial, dataFinal, descricao, eventColor) VALUES (%s, %s, %s, %s, %s)',
        (nomeEvento, dataInicial, dataFinal, descricao, eventColor)
    )
    conexao.commit()
    conexao.close()


    return jsonify({'message': 'Evento inserido com sucesso'}), 201


@app.route('/datas/<int:id>', methods=['PUT'])
def atualizar_evento(id):
    dados = request.get_json()


    nomeEvento = dados.get('nomeEvento')
    dataInicial = dados.get('dataInicial')
    dataFinal = dados.get('dataFinal')
    descricao = dados.get('descricao')
    eventColor = dados.get('eventColor', '#054161') # Obtém a cor ou usa a padrão


    # Validação básica
    if not nomeEvento or not dataInicial or not dataFinal:
        return jsonify({'erro': 'Campos obrigatórios faltando'}), 400


    conexao = get_db_connection()
    cursor = conexao.cursor()


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


    linhas_afetadas = cursor.rowcount


    cursor.close()
    conexao.close()


    if linhas_afetadas == 0:
        return jsonify({'erro': 'Evento não encontrado'}), 404


    return jsonify({'mensagem': 'Evento atualizado com sucesso'})


@app.route('/datas/<int:id>', methods=['DELETE'])
def deletar_evento(id):
    conexao = get_db_connection()
    cursor = conexao.cursor()


    sql = "DELETE FROM dados WHERE id = %s"
    valores = (id,)


    cursor.execute(sql, valores)
    conexao.commit()


    linhas_afetadas = cursor.rowcount


    cursor.close()
    conexao.close()


    if linhas_afetadas == 0:
        return jsonify({'erro': 'Evento não encontrado'}), 404


    return jsonify({'mensagem': 'Evento excluído com sucesso'})


@app.route('/datasFiltro', methods=['GET'])
def obter_evento_por_nome():
    nome_evento = request.args.get('nomeEvento')


    if not nome_evento:
        return jsonify({'erro': 'Parâmetro nomeEvento é obrigatório'}), 400


    conexao = get_db_connection()
    cursor = conexao.cursor(pymysql.cursors.DictCursor)


    sql = "SELECT * FROM dados WHERE nomeEvento LIKE %s"
    valor = ('%' + nome_evento + '%',)


    cursor.execute(sql, valor)
    rows = cursor.fetchall()


    cursor.close()
    conexao.close()


    eventos = []
    for row in rows:
        eventos.append({
            'id': row['id'],
            'nomeEvento': row['nomeEvento'],
            'dataInicial': row['dataInicial'],
            'dataFinal': row['dataFinal'],
            'descricao': row['descricao'],
            'eventColor': row.get('eventColor', '#054161') # Obtém a cor ou usa a padrão
        })


    return jsonify(eventos)


if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)
