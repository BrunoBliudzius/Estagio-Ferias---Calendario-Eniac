import os
import uuid
from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for, session
from flask_cors import CORS
import pymysql

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = 3600
CORS(app, supports_credentials=True)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "bmp", "tiff", "svg", "jfif"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="calendarioeniac",
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['nome']
        senha = request.form['senha']

        conexao = get_db_connection()
        with conexao.cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE usuario=%s AND senha=%s", (usuario, senha))
            user = cursor.fetchone()
        conexao.close()

        if user:
            session['usuario_id'] = user['id']
            session['usuario_nome'] = user['usuario']
            return redirect(url_for('novo_evento_page'))
        else:
            return "Usuário ou senha inválidos", 401

    return render_template("login.html")

@app.route('/novo-evento')
def novo_evento_page():
    if 'usuario_id' not in session:
        return redirect('/login')

    nome_formatado = session['usuario_nome'].title()

    return render_template("NovoEvento.html", usuario_nome=nome_formatado)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

def formatar_evento(row):
    imagem_url = row.get('imagem_url')
    if imagem_url:
        imagem_url = f"http://localhost:5000/uploads/{imagem_url}"
    return {
        'id': row['id'],
        'nomeEvento': row['nomeEvento'],
        'dataInicial': row['dataInicial'],
        'dataFinal': row['dataFinal'],
        'descricao': row['descricao'],
        'eventColor': row['eventColor'],
        'imagem_url': imagem_url,
        'usuario_nome': row.get('usuario')
    }

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/datas', methods=['GET'])
def obter_eventos():
    conexao = get_db_connection()
    cursor = conexao.cursor()
    # Faz um JOIN para buscar o nome do usuário
    cursor.execute('SELECT d.*, u.usuario FROM dados d LEFT JOIN usuarios u ON d.usuario_id = u.id')
    rows = cursor.fetchall()
    conexao.close()
    eventos = [formatar_evento(row) for row in rows]
    return jsonify(eventos)

@app.route('/datasFiltro', methods=['GET'])
def filtrar_eventos():
    nome_evento = request.args.get('nomeEvento', '').strip()

    conexao = get_db_connection()
    cursor = conexao.cursor()
    # Faz um JOIN para buscar o nome do usuário no filtro
    cursor.execute("SELECT d.*, u.usuario FROM dados d LEFT JOIN usuarios u ON d.usuario_id = u.id WHERE d.nomeEvento LIKE %s", (f"%{nome_evento}%",))
    rows = cursor.fetchall()
    conexao.close()

    eventos = [formatar_evento(row) for row in rows]
    return jsonify(eventos)

@app.route('/datas', methods=['POST'])
def criar_evento():
    if 'usuario_id' not in session:
        return jsonify({'erro': 'Não autorizado'}), 401

    usuario_id = session['usuario_id']
    nomeEvento = request.form.get('nomeEvento')
    dataInicial = request.form.get('dataInicial')
    dataFinal = request.form.get('dataFinal')
    descricao = request.form.get('descricao')
    eventColor = request.form.get('eventColor')

    imagem_url = None
    if 'imagem' in request.files:
        file = request.files['imagem']
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            unique_name = f"{uuid.uuid4()}.{ext}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
            file.save(filepath)
            imagem_url = unique_name

    conexao = get_db_connection()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO dados (nomeEvento, dataInicial, dataFinal, descricao, eventColor, imagem_url, usuario_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (nomeEvento, dataInicial, dataFinal, descricao, eventColor, imagem_url, usuario_id))
    conexao.commit()
    conexao.close()

    return jsonify({'mensagem': 'Evento criado com sucesso'}), 201

@app.route('/datas/<int:event_id>', methods=['PUT'])
def atualizar_evento(event_id):
    if 'usuario_id' not in session:
        return jsonify({'erro': 'Não autorizado'}), 401
        
    usuario_id = session['usuario_id']
    nomeEvento = request.form.get('nomeEvento')
    dataInicial = request.form.get('dataInicial')
    dataFinal = request.form.get('dataFinal')
    descricao = request.form.get('descricao')
    eventColor = request.form.get('eventColor')

    conexao = get_db_connection()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM dados WHERE id = %s", (event_id,))
    evento = cursor.fetchone()
    if not evento:
        conexao.close()
        return jsonify({'erro': 'Evento não encontrado'}), 404

    imagem_url = evento.get('imagem_url')
    if 'imagem' in request.files and request.files['imagem'].filename != '':
        file = request.files['imagem']
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            unique_name = f"{uuid.uuid4()}.{ext}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
            file.save(filepath)
            imagem_url = unique_name

    cursor.execute("""
        UPDATE dados
        SET nomeEvento = %s, dataInicial = %s, dataFinal = %s, descricao = %s, eventColor = %s, imagem_url = %s, usuario_id = %s
        WHERE id = %s
    """, (nomeEvento, dataInicial, dataFinal, descricao, eventColor, imagem_url, usuario_id, event_id))
    conexao.commit()
    conexao.close()

    return jsonify({'mensagem': 'Evento atualizado com sucesso'})

@app.route('/datas/<int:event_id>', methods=['DELETE'])
def deletar_evento(event_id):
    conexao = get_db_connection()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM dados WHERE id = %s", (event_id,))
    conexao.commit()
    conexao.close()
    return jsonify({'mensagem': 'Evento excluído com sucesso'})

if __name__ == '__main__':
    app.run(debug=True)