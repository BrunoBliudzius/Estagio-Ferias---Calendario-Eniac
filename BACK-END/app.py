import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # Permite OAuth em HTTP (desenvolvimento)
import uuid
from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for, session
from flask_cors import CORS
import pymysql
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime, date
import smtplib
from email.message import EmailMessage
from datetime import datetime


# Imports para a integração com o Google Agenda
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do app Flask
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", os.urandom(24))
app.permanent_session_lifetime = 3600
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuração da pasta de uploads
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Extensões permitidas
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "bmp", "tiff", "svg", "jfif"}

# Configuração do Google OAuth
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Função utilitária: verifica se o arquivo tem extensão permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Rota para exibir a página do calendário
@app.route('/calendario')
def calendario_page():
    return render_template("calendarioUser.html")

# Conexão com banco de dados
def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )

# Cliente da API OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Função auxiliar: soma/subtrai meses em uma data
def _add_months(d: date, months: int) -> date:
    y, m = d.year, d.month
    m += months
    y += (m - 1) // 12
    m = ((m - 1) % 12) + 1
    return date(y, m, 1)

# Rota de chat com IA
@app.route('/chat', methods=['POST'])
def chat():
    pergunta = request.json.get("pergunta")
    if not pergunta:
        return jsonify({"erro": "A pergunta não pode estar vazia."}), 400

    conexao = None
    try:
        conexao = get_db_connection()
        with conexao.cursor() as cursor:
            # Busca TODOS os eventos sem restrição de datas
            sql = """SELECT nomeEvento, dataInicial, dataFinal, descricao 
                     FROM dados 
                     ORDER BY dataInicial ASC"""
            cursor.execute(sql)
            eventos = cursor.fetchall()

        # Monta o contexto
        contexto = "Com base APENAS nos seguintes eventos do calendário, responda à pergunta do usuário.\n"
        if not eventos:
            contexto += "Nenhum evento encontrado no calendário.\n"
        else:
            for e in eventos:
                data_ini = e['dataInicial'].strftime('%d/%m/%Y %H:%M') if isinstance(e['dataInicial'], datetime) else e['dataInicial']
                data_fim = e['dataFinal'].strftime('%d/%m/%Y %H:%M') if isinstance(e['dataFinal'], datetime) else e['dataFinal']
                contexto += f"- Título: {e['nomeEvento']}, Início: {data_ini}, Fim: {data_fim}, Descrição: {e['descricao']}\n"

        data_atual_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        prompt_sistema = f"Você é um assistente de calendário prestativo. A data e hora atual é {data_atual_str}. Responda de forma concisa e amigável."

        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": f"Contexto dos eventos:\n{contexto}\n\nPergunta do usuário: {pergunta}"}
            ],
            temperature=0.4
        )
        return jsonify({"resposta": resposta.choices[0].message.content})

    except pymysql.Error:
        return jsonify({"erro": "Ocorreu um erro ao acessar o banco de dados."}), 500
    except Exception:
        return jsonify({"erro": "Ocorreu um erro inesperado no servidor."}), 500
    finally:
        if conexao:
            conexao.close()


# Rota de login
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
            session['user_role'] = user.get('role', 'user')
            return redirect(url_for('novo_evento_page'))
        else:
            return "Usuário ou senha inválidos", 401
    return render_template("login.html")

# Rota que verifica se o usuário é admin
@app.route('/check-admin-status', methods=['GET'])
def check_admin_status():
    if 'user_role' in session and session['user_role'] == 'admin':
        return jsonify({'isAdmin': True})
    return jsonify({'isAdmin': False})

# Página de criação de novo evento
@app.route('/novo-evento')
def novo_evento_page():
    if 'usuario_id' not in session:
        return redirect('/login')
    nome_formatado = session['usuario_nome'].title()
    return render_template("NovoEvento.html", usuario_nome=nome_formatado)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# Função auxiliar: converte datas para formato ISO 8601
def _to_iso8601(value):
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return datetime(value.year, value.month, value.day).isoformat()
    return value

def calcular_semana_do_ano(data_str):
    data = datetime.fromisoformat(data_str)
    return data.isocalendar()[1]  # número da semana (1 a 53)

def calcular_dia_da_semana(data_str):
    data = datetime.fromisoformat(data_str)
    return data.isoweekday()  # 1=segunda ... 7=domingo

# Formata um evento para JSON
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

# Rota para servir arquivos de upload
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

# Rota GET que filtra eventos
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
    repetir = request.form.get('repetir_anualmente', '0') == '1'
    semana_do_ano = calcular_semana_do_ano(dataInicial)
    dia_da_semana = calcular_dia_da_semana(dataInicial)

    # Enviar email para os participantes (se houver)
    remetente = "brunosilvabliu@gmail.com"
    emails_raw = request.form.get('email')  # pode vir 1 ou vários e-mails separados por vírgula
    assunto = "Convite para o Evento"
    mensagem = (
        f"Olá, estou enviando esse email para informar que você foi convidado para o evento: "
        f"{nomeEvento}, que ocorrerá de {dataInicial} até {dataFinal}. "
        f"Descrição do evento: {descricao}."
    )
    senha = "bajo zusc ygzw fyqz"

    if emails_raw:  # só tenta enviar se não for vazio
        # separa por vírgula e remove espaços vazios
        emails = [e.strip() for e in emails_raw.split(",") if e.strip()]

        if emails:  # garante que tem destinatários válidos
            msg = EmailMessage()
            msg['From'] = remetente
            msg['To'] = ", ".join(emails)  # cabeçalho visível no e-mail
            msg['Subject'] = assunto
            msg.set_content(mensagem)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as email:
                email.login(remetente, senha)
                email.send_message(msg)

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
    if repetir:
        ano_base = datetime.fromisoformat(dataInicial).year
    for ano in range(ano_base, ano_base + 10):  # repetir próximos  anos
        # gera a data correspondente no ano "ano"
        data_ini = datetime.fromisocalendar(ano, semana_do_ano, dia_da_semana)
        data_fim = data_ini + (datetime.fromisoformat(dataFinal) - datetime.fromisoformat(dataInicial))

        cursor.execute("""
            INSERT INTO dados (nomeEvento, dataInicial, dataFinal, descricao, eventColor, imagem_url, usuario_id, semana_do_ano, dia_da_semana, repetir_anualmente)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
        """, (nomeEvento, data_ini, data_fim, descricao, eventColor, imagem_url, usuario_id, semana_do_ano, dia_da_semana))
    else:
        cursor.execute("""
        INSERT INTO dados (nomeEvento, dataInicial, dataFinal, descricao, eventColor, imagem_url, usuario_id, semana_do_ano, dia_da_semana, repetir_anualmente)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 0)
    """, (nomeEvento, dataInicial, dataFinal, descricao, eventColor, imagem_url, usuario_id, semana_do_ano, dia_da_semana))
    conexao.commit()
    conexao.close()

    return jsonify({'mensagem': 'Evento criado com sucesso'}), 201


# Rota PUT para atualizar um evento
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

# Rota DELETE para excluir um evento
@app.route('/datas/<int:event_id>', methods=['DELETE'])
def deletar_evento(event_id):
    conexao = get_db_connection()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM dados WHERE id = %s", (event_id,))
    conexao.commit()
    conexao.close()
    return jsonify({'mensagem': 'Evento excluído com sucesso'})
    
# Rota para iniciar a autenticação com o Google
@app.route('/google-login')
def google_login():
    client_config = {
        "web": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost:5000/google-callback"]
        }
    }
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        client_config, scopes=SCOPES)
    
    flow.redirect_uri = url_for('google_callback', _external=True)
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    session['state'] = state
    return redirect(authorization_url)

# Rota de callback do Google
@app.route('/google-callback')
def google_callback():
    state = session['state']
    client_config = {
        "web": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost:5000/google-callback"]
        }
    }
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        client_config, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('google_callback', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session['google_credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

    return redirect(url_for('import_google_calendar'))

# ROTA PARA IMPORTAR OS EVENTOS DO GOOGLE AGENDA (VERSÃO FINAL E SEGURA)
@app.route('/import-google-calendar')
def import_google_calendar():
    if 'google_credentials' not in session:
        return redirect(url_for('google_login'))

    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    credentials = google.oauth2.credentials.Credentials(**session['google_credentials'])
    
    try:
        service = build('calendar', 'v3', credentials=credentials)
        now = datetime.utcnow().isoformat() + 'Z'
        
        events_result = service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=50, singleEvents=True,
            orderBy='startTime'
        ).execute()
        google_events = events_result.get('items', [])

        if not google_events:
            return redirect(url_for('calendario_page'))

        conexao = get_db_connection()
        cursor = conexao.cursor()
        current_user_id = session['usuario_id']

        # Pega os IDs dos eventos que serão importados
        google_event_ids = [event['id'] for event in google_events]

        # 1. DELETA os eventos antigos do Google que pertencem a este usuário
        # Isso garante que se um evento for cancelado no Google, ele será removido aqui.
        if google_event_ids:
            # O placeholder %s será expandido para a quantidade correta de IDs
            format_strings = ','.join(['%s'] * len(google_event_ids))
            delete_sql = f"""
                DELETE FROM dados 
                WHERE usuario_id = %s AND google_event_id IS NOT NULL
            """
            cursor.execute(delete_sql, (current_user_id,))

        # 2. INSERE a lista de eventos mais recente do Google
        eventos_para_inserir = []
        for event in google_events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            
            eventos_para_inserir.append((
                event.get('summary', 'Evento do Google'),
                start,
                end,
                event.get('description', ''),
                '#34a853', # Cor verde para eventos do Google
                current_user_id,
                event['id']
            ))

        if eventos_para_inserir:
            insert_sql = """
                INSERT INTO dados (nomeEvento, dataInicial, dataFinal, descricao, eventColor, usuario_id, google_event_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.executemany(insert_sql, eventos_para_inserir)
        
        conexao.commit()
        cursor.close()
        conexao.close()

        return redirect(url_for('calendario_page'))

    except HttpError as error:
        print(f'Ocorreu um erro: {error}')
        return "Ocorreu um erro ao buscar os eventos do Google Agenda.", 500

# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)