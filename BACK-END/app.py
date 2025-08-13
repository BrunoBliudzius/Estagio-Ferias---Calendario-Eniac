import os
import uuid
from flask import Flask, request, jsonify, send_from_directory, render_template,redirect, url_for, session
from flask_cors import CORS
import pymysql

# Configuração do Flask
app = Flask(__name__)

# Chave secreta obrigatória para sessões
app.secret_key = os.urandom(24)  # pode trocar por uma fixa se quiser manter entre reinícios

# Configurar sessão para expirar depois de um tempo (opcional)
app.permanent_session_lifetime = 3600  # em segundos (1 hora)

# CORS com suporte a cookies
CORS(app, supports_credentials=True)

# Pasta onde as imagens serão salvas
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Extensões permitidas
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "bmp", "tiff", "svg", "jfif"}

# Função para verificar se extensão é válida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Função de conexão com banco
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="calendarioeniac",
        cursorclass=pymysql.cursors.DictCursor
    )

# Rota para login
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
            return redirect(url_for('novo_evento_page'))  # Redireciona para a rota correta
        else:
            return "Usuário ou senha inválidos", 401

    # GET: Serve a página de login
    return render_template("login.html")

@app.route('/novo-evento')
def novo_evento_page():
    if 'usuario_id' not in session:
        return redirect('/login')
    return render_template("NovoEvento.html", usuario_nome=session['usuario_nome'])


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# Formata evento para o front
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
        'imagem_url': imagem_url
    }

# Rota para servir imagens
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Rota GET para listar eventos
@app.route('/datas', methods=['GET'])
def obter_eventos():
    conexao = get_db_connection()
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM dados')
    rows = cursor.fetchall()
    conexao.close()
    eventos = [formatar_evento(row) for row in rows]
    return jsonify(eventos)

# Rota POST para criar evento com imagem
@app.route('/datas', methods=['POST'])
def criar_evento():
    nomeEvento = request.form.get('nomeEvento')
    dataInicial = request.form.get('dataInicial')
    dataFinal = request.form.get('dataFinal')
    descricao = request.form.get('descricao')
    eventColor = request.form.get('eventColor')

    # Upload de imagem
    imagem_url = None
    if 'imagem' in request.files:
        file = request.files['imagem']
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            unique_name = f"{uuid.uuid4()}.{ext}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
            file.save(filepath)
            imagem_url = unique_name  # salva só o nome no banco

    conexao = get_db_connection()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO dados (nomeEvento, dataInicial, dataFinal, descricao, eventColor, imagem_url)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nomeEvento, dataInicial, dataFinal, descricao, eventColor, imagem_url))
    conexao.commit()
    conexao.close()

    return jsonify({'mensagem': 'Evento criado com sucesso'}), 201

# Rota PUT para atualizar evento
@app.route('/datas/<int:event_id>', methods=['PUT'])
def atualizar_evento(event_id):
    nomeEvento = request.form.get('nomeEvento')
    dataInicial = request.form.get('dataInicial')
    dataFinal = request.form.get('dataFinal')
    descricao = request.form.get('descricao')
    eventColor = request.form.get('eventColor')

    conexao = get_db_connection()
    cursor = conexao.cursor()

    # Verifica se evento existe
    cursor.execute("SELECT * FROM dados WHERE id = %s", (event_id,))
    evento = cursor.fetchone()
    if not evento:
        conexao.close()
        return jsonify({'erro': 'Evento não encontrado'}), 404

    imagem_url = evento.get('imagem_url')

    # Upload de nova imagem
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
        SET nomeEvento = %s, dataInicial = %s, dataFinal = %s, descricao = %s, eventColor = %s, imagem_url = %s
        WHERE id = %s
    """, (nomeEvento, dataInicial, dataFinal, descricao, eventColor, imagem_url, event_id))
    conexao.commit()
    conexao.close()

    return jsonify({'mensagem': 'Evento atualizado com sucesso'})

# Rota DELETE para excluir evento
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