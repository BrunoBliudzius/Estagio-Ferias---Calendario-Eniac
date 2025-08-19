import os
import uuid
from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for, session
from flask_cors import CORS
import pymysql
from openai import OpenAI
from dotenv import load_dotenv # Importa a biblioteca para carregar o .env
from datetime import datetime, date # Importa para trabalhar com datas

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
# A chave secreta também pode vir de uma variável de ambiente para mais segurança
app.secret_key = os.getenv("FLASK_SECRET_KEY", os.urandom(24))
app.permanent_session_lifetime = 3600
CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "bmp", "tiff", "svg", "jfif"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/calendario')
def calendario_page():
    return render_template("calendarioUser.html")

def get_db_connection():
    # CORREÇÃO DE SEGURANÇA: Busca os dados do banco a partir das variáveis de ambiente
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )

# CORREÇÃO DE SEGURANÇA: A chave da API é lida de forma segura do arquivo .env
# NUNCA COLOQUE A CHAVE DA API DIRETAMENTE NO CÓDIGO!
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ==============================
# ALTERAÇÃO: helpers de data p/ janela de meses
# ==============================
def _add_months(d: date, months: int) -> date:
    """Adiciona (ou subtrai) meses a uma data sem libs externas."""
    y, m = d.year, d.month
    m += months
    # normaliza ano/mes
    y += (m - 1) // 12
    m = ((m - 1) % 12) + 1
    # garante dia válido (aqui fixamos 1 para usar em 'primeiro dia do mês')
    return date(y, m, 1)

@app.route('/chat', methods=['POST'])
def chat():
    pergunta = request.json.get("pergunta")
    if not pergunta:
        return jsonify({"erro": "A pergunta não pode estar vazia."}), 400

    conexao = None # Inicializa a conexão como None
    try:
        # 1. Buscar eventos do banco (com filtro de performance)
        conexao = get_db_connection()
        with conexao.cursor() as cursor:
            # MELHORIA DE PERFORMANCE (ALTERAÇÃO):
            # Em vez de "somente mês atual", buscamos uma janela de -6 a +6 meses,
            # o que permite responder sobre meses anteriores/posteriores mantendo o contexto enxuto.
            hoje = date.today()
            janela_inicio = _add_months(hoje, -6)  # primeiro dia do mês de 6 meses atrás
            janela_fim_exclusivo = _add_months(hoje, +7)  # primeiro dia do mês após +6 meses (limite exclusivo)

            # ALTERAÇÃO: usamos intervalo [>= inicio, < fim_exclusivo] para performant e correto
            sql = """
                SELECT nomeEvento, dataInicial, dataFinal, descricao
                FROM dados
                WHERE dataInicial >= %s AND dataInicial < %s
                ORDER BY dataInicial ASC
            """
            cursor.execute(sql, (janela_inicio, janela_fim_exclusivo))
            eventos = cursor.fetchall()

        # 2. Montar contexto com os eventos
        contexto = "Com base APENAS nos seguintes eventos do calendário, responda à pergunta do usuário.\n"
        contexto += f"Eventos cadastrados na janela {janela_inicio.strftime('%m/%Y')} a {(_add_months(hoje, +6)).strftime('%m/%Y')}:\n"
        if not eventos:
            contexto += "Nenhum evento encontrado na janela considerada.\n"
        else:
            for e in eventos:
                # Formata as datas para um formato mais legível se não forem strings
                data_ini = e['dataInicial'].strftime('%d/%m/%Y %H:%M') if isinstance(e['dataInicial'], datetime) else e['dataInicial']
                data_fim = e['dataFinal'].strftime('%d/%m/%Y %H:%M') if isinstance(e['dataFinal'], datetime) else e['dataFinal']
                contexto += f"- Título: {e['nomeEvento']}, Início: {data_ini}, Fim: {data_fim}, Descrição: {e['descricao']}\n"

        # MELHORIA DE CONTEXTO: Informar a data atual para a IA
        data_atual_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        prompt_sistema = f"Você é um assistente de calendário prestativo. A data e hora atual é {data_atual_str}. Responda de forma concisa e amigável."

        # 3. Mandar para a IA
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
        # Tratamento de erro para o banco de dados
        print(f"Erro de banco de dados: {db_err}")
        return jsonify({"erro": "Ocorreu um erro ao acessar o banco de dados."}), 500
    except Exception as e:
        # Tratamento de erro genérico
        print(f"Ocorreu um erro inesperado: {e}")
        return jsonify({"erro": "Ocorreu um erro inesperado no servidor."}), 500
    finally:
        # Garante que a conexão com o banco seja sempre fechada
        if conexao:
            conexao.close()


# --- O restante do seu código permanece o mesmo, pois já estava muito bom! ---
# ... (cole aqui todas as outras rotas: /login, /check-admin-status, /novo-evento, etc.) ...
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['nome']
        senha = request.form['senha']

        conexao = get_db_connection()
        with conexao.cursor() as cursor:
            # Seleciona o usuário e seu papel (role)
            cursor.execute("SELECT * FROM usuarios WHERE usuario=%s AND senha=%s", (usuario, senha))
            user = cursor.fetchone()
        conexao.close()

        if user:
            session['usuario_id'] = user['id']
            session['usuario_nome'] = user['usuario']
            # Armazena o papel do usuário na sessão
            session['user_role'] = user.get('role', 'user') 
            return redirect(url_for('novo_evento_page'))
        else:
            return "Usuário ou senha inválidos", 401
    return render_template("login.html")

@app.route('/check-admin-status', methods=['GET'])
def check_admin_status():
    # Verifica se o usuário está logado E se tem a role de 'admin'
    if 'user_role' in session and session['user_role'] == 'admin':
        return jsonify({'isAdmin': True})
    return jsonify({'isAdmin': False})

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

# ==============================
# ALTERAÇÃO: util p/ serializar datas em ISO 8601 no JSON
# ==============================
def _to_iso8601(value):
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        # normaliza para meia-noite local
        return datetime(value.year, value.month, value.day).isoformat()
    return value

def formatar_evento(row, is_admin=False):
    imagem_url = row.get('imagem_url')
    if imagem_url:
        # ALTERAÇÃO: monta URL da imagem baseada no host atual (mais robusto que localhost fixo)
        base = request.host_url.rstrip('/')
        imagem_url = f"{base}/uploads/{imagem_url}"
    
    evento = {
        'id': row['id'],
        'nomeEvento': row['nomeEvento'],
        # ALTERAÇÃO: garante strings ISO p/ compatibilidade com FullCalendar/JSON
        'dataInicial': _to_iso8601(row['dataInicial']),
        'dataFinal': _to_iso8601(row['dataFinal']),
        'descricao': row['descricao'],
        'eventColor': row['eventColor'],
        'imagem_url': imagem_url,
    }
    # Somente adiciona o nome do usuário se for admin
    if is_admin:
        evento['usuario_nome'] = row.get('usuario')
    return evento

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/datas', methods=['GET'])
def obter_eventos():
    # A verificação de admin é feita com base na sessão
    is_admin = 'user_role' in session and session['user_role'] == 'admin'
    conexao = get_db_connection()
    cursor = conexao.cursor()
    cursor.execute('SELECT d.*, u.usuario FROM dados d LEFT JOIN usuarios u ON d.usuario_id = u.id')
    rows = cursor.fetchall()
    conexao.close()
    eventos = [formatar_evento(row, is_admin) for row in rows]
    return jsonify(eventos)

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
