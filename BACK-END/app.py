import os
import uuid
from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for, session
from flask_cors import CORS
import pymysql
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime, date

# Carrega variáveis de ambiente do arquivo .env (como senhas e chaves)
load_dotenv()

# Configuração do app Flask
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", os.urandom(24))  # Chave usada para sessões
app.permanent_session_lifetime = 3600  # Tempo de expiração da sessão
CORS(app, resources={r"/*": {"origins": "*"}})  # Permite requisições externas (CORS liberado)

# Configuração da pasta de uploads (imagens de eventos)
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Extensões permitidas para upload de imagens
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "bmp", "tiff", "svg", "jfif"}

# Função utilitária: verifica se o arquivo tem extensão permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Rota para exibir a página do calendário
@app.route('/calendario')
def calendario_page():
    return render_template("calendarioUser.html")

# Conexão com banco de dados usando variáveis de ambiente
def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )

# Cliente da API OpenAI (para o chat do calendário inteligente)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Função auxiliar: soma/subtrai meses em uma data (para calcular janelas de eventos)
def _add_months(d: date, months: int) -> date:
    y, m = d.year, d.month
    m += months
    y += (m - 1) // 12
    m = ((m - 1) % 12) + 1
    return date(y, m, 1)

# Rota de chat com IA (responde perguntas sobre os eventos)
@app.route('/chat', methods=['POST'])
def chat():
    pergunta = request.json.get("pergunta")  # Pergunta do usuário
    if not pergunta:
        return jsonify({"erro": "A pergunta não pode estar vazia."}), 400

    conexao = None
    try:
        # Busca eventos do banco em uma janela de -6 a +6 meses
        conexao = get_db_connection()
        with conexao.cursor() as cursor:
            hoje = date.today()
            janela_inicio = _add_months(hoje, -6)
            janela_fim_exclusivo = _add_months(hoje, +7)

            sql = """
                SELECT nomeEvento, dataInicial, dataFinal, descricao
                FROM dados
                WHERE dataInicial >= %s AND dataInicial < %s
                ORDER BY dataInicial ASC
            """
            cursor.execute(sql, (janela_inicio, janela_fim_exclusivo))
            eventos = cursor.fetchall()

        # Monta o contexto que será enviado para a IA
        contexto = "Com base APENAS nos seguintes eventos do calendário, responda à pergunta do usuário.\n"
        contexto += f"Eventos cadastrados na janela {janela_inicio.strftime('%m/%Y')} a {(_add_months(hoje, +6)).strftime('%m/%Y')}:\n"
        if not eventos:
            contexto += "Nenhum evento encontrado na janela considerada.\n"
        else:
            for e in eventos:
                data_ini = e['dataInicial'].strftime('%d/%m/%Y %H:%M') if isinstance(e['dataInicial'], datetime) else e['dataInicial']
                data_fim = e['dataFinal'].strftime('%d/%m/%Y %H:%M') if isinstance(e['dataFinal'], datetime) else e['dataFinal']
                contexto += f"- Título: {e['nomeEvento']}, Início: {data_ini}, Fim: {data_fim}, Descrição: {e['descricao']}\n"

        # Adiciona data/hora atual no prompt
        data_atual_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        prompt_sistema = f"Você é um assistente de calendário prestativo. A data e hora atual é {data_atual_str}. Responda de forma concisa e amigável."

        # Envia para IA responder
        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": f"Contexto dos eventos:\n{contexto}\n\nPergunta do usuário: {pergunta}"}
            ],
            temperature=0.1
        )
        return jsonify({"resposta": resposta.choices[0].message.content})

    except pymysql.Error as db_err:
        return jsonify({"erro": "Ocorreu um erro ao acessar o banco de dados."}), 500
    except Exception as e:
        return jsonify({"erro": "Ocorreu um erro inesperado no servidor."}), 500
    finally:
        if conexao:
            conexao.close()

# Rota de login (cria sessão do usuário)
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
            session['user_role'] = user.get('role', 'user')  # Guarda se é admin ou não
            return redirect(url_for('novo_evento_page'))
        else:
            return "Usuário ou senha inválidos", 401
    return render_template("login.html")

# Rota que verifica se o usuário logado é admin
@app.route('/check-admin-status', methods=['GET'])
def check_admin_status():
    if 'user_role' in session and session['user_role'] == 'admin':
        return jsonify({'isAdmin': True})
    return jsonify({'isAdmin': False})

# Página de criação de novo evento (só acessível logado)
@app.route('/novo-evento')
def novo_evento_page():
    if 'usuario_id' not in session:
        return redirect('/login')
    nome_formatado = session['usuario_nome'].title()
    return render_template("NovoEvento.html", usuario_nome=nome_formatado)

# Logout (limpa sessão do usuário)
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# Função auxiliar: converte datas em formato ISO 8601 para JSON
def _to_iso8601(value):
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return datetime(value.year, value.month, value.day).isoformat()
    return value

# Função para formatar um evento em JSON
def formatar_evento(row, is_admin=False):
    imagem_url = row.get('imagem_url')
    if imagem_url:
        base = request.host_url.rstrip('/')
        imagem_url = f"{base}/uploads/{imagem_url}"
    
    evento = {
        'id': row['id'],
        'nomeEvento': row['nomeEvento'],
        'dataInicial': _to_iso8601(row['dataInicial']),
        'dataFinal': _to_iso8601(row['dataFinal']),
        'descricao': row['descricao'],
        'eventColor': row['eventColor'],
        'imagem_url': imagem_url,
    }
    if is_admin:
        evento['usuario_nome'] = row.get('usuario')
    return evento

# Rota para servir arquivos de upload (imagens)
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Rota GET que retorna todos os eventos
@app.route('/datas', methods=['GET'])
def obter_eventos():
    is_admin = 'user_role' in session and session['user_role'] == 'admin'
    conexao = get_db_connection()
    cursor = conexao.cursor()
    cursor.execute('SELECT d.*, u.usuario FROM dados d LEFT JOIN usuarios u ON d.usuario_id = u.id')
    rows = cursor.fetchall()
    conexao.close()
    eventos = [formatar_evento(row, is_admin) for row in rows]
    return jsonify(eventos)

# Rota GET que filtra eventos pelo nome
@app.route('/datasFiltro', methods=['GET'])
def filtrar_eventos():
    is_admin = 'user_role' in session and session['user_role'] == 'admin'
    nome_evento = request.args.get('nomeEvento', '').strip()

    conexao = get_db_connection()
    cursor = conexao.cursor()
    cursor.execute("SELECT d.*, u.usuario FROM dados d LEFT JOIN usuarios u ON d.usuario_id = u.id WHERE d.nomeEvento LIKE %s", (f"%{nome_evento}%",))
    rows = cursor.fetchall()
    conexao.close()

    eventos = [formatar_evento(row, is_admin) for row in rows]
    return jsonify(eventos)

# Rota POST para criar um novo evento
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

    # Upload da imagem do evento
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

# Rota PUT para atualizar um evento existente
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

    # Atualiza imagem caso seja enviada uma nova
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

# Rota DELETE para excluir um evento
@app.route('/datas/<int:event_id>', methods=['DELETE'])
def deletar_evento(event_id):
    conexao = get_db_connection()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM dados WHERE id = %s", (event_id,))
    conexao.commit()
    conexao.close()
    return jsonify({'mensagem': 'Evento excluído com sucesso'})

# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)