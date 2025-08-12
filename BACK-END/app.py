from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
import os
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
CORS(app, supports_credentials=True)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def db():
    return pymysql.connect(
        host='localhost',
                user='root',
        password='',
        db='calendarioeniac',
        cursorclass=pymysql.cursors.DictCursor
    )

def formatar_evento(row):
    return {
        'id': row['id'],
        'nomeEvento': row['nomeEvento'],
        'dataInicial': row['dataInicial'],
        'dataFinal': row['dataFinal'],
        'descricao': row['descricao'],
        'eventColor': row['eventColor'],
        'imagem_url': row.get('imagem_url')
    }

@app.route('/datas', methods=['GET'])
def listar_eventos():
    with db() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("SELECT * FROM dados")
            eventos = [formatar_evento(row) for row in cursor.fetchall()]
    return jsonify(eventos)

@app.route('/datas', methods=['POST'])
def criar_evento():
    nomeEvento = request.form.get('nomeEvento')
    dataInicial = request.form.get('dataInicial')
    dataFinal = request.form.get('dataFinal')
    descricao = request.form.get('descricao', '')
    eventColor = request.form.get('eventColor', '#3788d8')

    if not nomeEvento or not dataInicial or not dataFinal:
        return jsonify({'erro': 'Campos obrigatórios faltando'}), 400

    imagem_url = None

    if 'imagem' in request.files:
        file = request.files['imagem']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ext = filename.rsplit('.', 1)[1].lower()
            unique_name = f"{uuid.uuid4()}.{ext}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
            file.save(filepath)
            imagem_url = f"{UPLOAD_FOLDER}/{unique_name}"

    with db() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("""
                INSERT INTO dados (nomeEvento, dataInicial, dataFinal, descricao, eventColor, imagem_url)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nomeEvento, dataInicial, dataFinal, descricao, eventColor, imagem_url))
            conexao.commit()
    return jsonify({'mensagem': 'Evento criado com sucesso'}), 201

@app.route('/datas/<int:id>', methods=['PUT'])
def atualizar_evento(id):
    dados = request.get_json()
    campos = ['nomeEvento', 'dataInicial', 'dataFinal']
    if not all(dados.get(campo) for campo in campos):
        return jsonify({'erro': 'Campos obrigatórios faltando'}), 400

    with db() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("""
                UPDATE dados
                SET nomeEvento = %s, dataInicial = %s, dataFinal = %s, descricao = %s, eventColor = %s
                WHERE id = %s
            """, (dados['nomeEvento'], dados['dataInicial'], dados['dataFinal'], dados.get('descricao', ''), dados.get('eventColor'), id))
            conexao.commit()
            if cursor.rowcount == 0:
                return jsonify({'erro': 'Evento não encontrado'}), 404
    return jsonify({'mensagem': 'Evento atualizado com sucesso'})

@app.route('/datas/<int:id>', methods=['DELETE'])
def deletar_evento(id):
    with db() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("DELETE FROM dados WHERE id = %s", (id,))
            conexao.commit()
            if cursor.rowcount == 0:
                return jsonify({'erro': 'Evento não encontrado'}), 404
    return jsonify({'mensagem': 'Evento excluído com sucesso'})

@app.route('/datasFiltro', methods=['GET'])
def buscar_evento_por_nome():
    nome = request.args.get('nomeEvento')
    if not nome:
        return jsonify({'erro': 'Parâmetro nomeEvento é obrigatório'}), 400

    with db() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("SELECT * FROM dados WHERE nomeEvento LIKE %s", ('%' + nome + '%',))
            eventos = [formatar_evento(row) for row in cursor.fetchall()]
    return jsonify(eventos)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
