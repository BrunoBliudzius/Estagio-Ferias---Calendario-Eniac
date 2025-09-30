import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # Permite OAuth em HTTP (desenvolvimento)
import uuid
from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for, session
from flask_cors import CORS
import pymysql
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime, date, timedelta # TIMEDELTA JÁ ESTÁ AQUI
import smtplib
from email.message import EmailMessage

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

# Rota de chat com IA (VERSÃO CORRIGIDA E INTELIGENTE)
@app.route('/chat', methods=['POST'])
def chat():
    pergunta = request.json.get("pergunta")
    if not pergunta:
        return jsonify({"erro": "A pergunta não pode estar vazia."}), 400

    conexao = None
    try:
        # ETAPA 1: Usar a IA para extrair informações da pergunta do usuário
        prompt_extracao = f"""
        Extraia o ano e o número da semana da seguinte pergunta do usuário.
        Responda APENAS com um objeto JSON com as chaves "ano" e "semana".
        Se não encontrar um ano, use o ano atual ({datetime.now().year}).
        Se não encontrar um número de semana, a chave "semana" deve ser null.
        Pergunta: "{pergunta}"
        """
        
        response_extracao = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt_extracao}]
        )
        
        try:
            dados_extraidos = json.loads(response_extracao.choices[0].message.content)
            ano = dados_extraidos.get("ano")
            semana = dados_extraidos.get("semana")
        except (json.JSONDecodeError, AttributeError):
            # Se a IA não retornar um JSON válido, faz uma busca genérica
            ano = None
            semana = None

        # ETAPA 2: Construir uma consulta SQL precisa com base nos dados extraídos
        conexao = get_db_connection()
        with conexao.cursor() as cursor:
            sql = "SELECT nomeEvento, dataInicial, dataFinal, descricao FROM dados WHERE "
            params = []
            
            if ano and semana:
                # O modo 1 do WEEK() considera a semana começando na Segunda-feira, igual ao isocalendar
                sql += "YEAR(dataInicial) = %s AND WEEK(dataInicial, 1) = %s"
                params.extend([ano, semana])
            elif ano:
                sql += "YEAR(dataInicial) = %s"
                params.append(ano)
            else:
                # Se não extrair nada, busca pelo nome do evento na pergunta
                sql += "nomeEvento LIKE %s"
                params.append(f"%{pergunta}%")

            sql += " ORDER BY dataInicial ASC"
            cursor.execute(sql, tuple(params))
            eventos = cursor.fetchall()

        # ETAPA 3: Montar o contexto APENAS com os eventos corretos e gerar a resposta final
        contexto = ""
        if not eventos:
            contexto = "Nenhum evento foi encontrado para a sua pesquisa.\n"
        else:
            contexto += "Com base nos seguintes eventos encontrados, responda à pergunta do usuário:\n"
            for e in eventos:
                data_ini = e['dataInicial'].strftime('%d/%m/%Y') if isinstance(e['dataInicial'], (datetime, date)) else e['dataInicial']
                data_fim = e['dataFinal'].strftime('%d/%m/%Y') if isinstance(e['dataFinal'], (datetime, date)) else e['dataFinal']
                contexto += f"- Título: {e['nomeEvento']}, Início: {data_ini}, Fim: {data_fim}\n"

        data_atual_str = datetime.now().strftime("%d/%m/%Y")
        prompt_final = f"""
        Você é um assistente de calendário amigável. A data atual é {data_atual_str}.
        Seu colega (o banco de dados) já fez a pesquisa e encontrou os seguintes resultados.
        Sua única tarefa é apresentar esses resultados de forma clara e concisa para o usuário.
        Não adicione nenhuma informação que não esteja listada abaixo.

        Resultados da pesquisa:
        {contexto}

        Pergunta original do usuário: "{pergunta}"
        """

        resposta_final = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt_final}],
            temperature=0.2 # Temperatura mais baixa para ser mais direto e menos criativo
        )

        return jsonify({"resposta": resposta_final.choices[0].message.content})

    except pymysql.Error as db_error:
        print(f"Erro de Banco de Dados: {db_error}")
        return jsonify({"erro": "Ocorreu um erro ao acessar o banco de dados."}), 500
    except Exception as e:
        print(f"Erro Inesperado: {e}")
        return jsonify({"erro": "Ocorreu um erro inesperado no servidor."}), 500
    finally:
        if 'conexao' in locals() and conexao and conexao.open:
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
            tipo_usuario = user.get('tipo_usuario', 'externo')
            session['tipo_usuario'] = tipo_usuario

            if tipo_usuario == 'aluno':
                return redirect(url_for('calendario_page'))
            else:
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
def _to_iso_8601(value):
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        # Para garantir consistência, formatamos a data para o início do dia
        return datetime(value.year, value.month, value.day).isoformat()
    return value


def calcular_semana_do_ano(data_str):
    date_part = data_str[:10]
    data_obj = date.fromisoformat(date_part)
    return data_obj.isocalendar()[1]

def calcular_dia_da_semana(data_str):
    date_part = data_str[:10]
    data_obj = date.fromisoformat(date_part)
    return data_obj.isoweekday()

# Formata um evento para JSON
def formatar_evento(row, is_admin=False):
    imagem_url = row.get('imagem_url')
    if imagem_url:
        base = request.host_url.rstrip('/')
        imagem_url = f"{base}/uploads/{imagem_url}"
    
    evento = {
        'id': row['id'],
        'nomeEvento': row['nomeEvento'],
        'dataInicial': _to_iso_8601(row['dataInicial']),
        'dataFinal': _to_iso_8601(row['dataFinal']),
        'descricao': row['descricao'],
        'eventColor': row['eventColor'],
        'imagem_url': imagem_url,
        'evento_tipo': row.get('evento_tipo', 'externo') # Adicionado
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
    tipo_usuario = session.get('tipo_usuario', 'externo')

    conexao = get_db_connection()
    cursor = conexao.cursor()

    if tipo_usuario == 'admin':
        cursor.execute('SELECT d.*, u.usuario FROM dados d LEFT JOIN usuarios u ON d.usuario_id = u.id')
    else:
        # Usando FIND_IN_SET para buscar o tipo de usuário na string de evento_tipo
        cursor.execute("SELECT d.*, u.usuario FROM dados d LEFT JOIN usuarios u ON d.usuario_id = u.id WHERE FIND_IN_SET(%s, d.evento_tipo)", (tipo_usuario,))


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
    if 'usuario_id' not in session or session.get('tipo_usuario') != 'admin':
        return jsonify({'erro': 'Não autorizado'}), 401

    usuario_id = session['usuario_id']
    nomeEvento = request.form.get('nomeEvento')
    dataInicial_str = request.form.get('dataInicial')
    dataFinal_str = request.form.get('dataFinal')
    descricao = request.form.get('descricao')
    eventColor = request.form.get('eventColor')
    repetir = request.form.get('repetir_anualmente', '0') == '1'
    evento_tipos = request.form.getlist('evento_tipo')

    if not evento_tipos:
        return jsonify({'erro': 'Selecione ao menos uma opção de visibilidade (Aluno, Externo ou Admin).'}), 400
    
    evento_tipo_str = ",".join(evento_tipos)

    data_inicial_obj = date.fromisoformat(dataInicial_str[:10])
    data_final_obj = date.fromisoformat(dataFinal_str[:10])
    
    if data_final_obj > data_inicial_obj:
        data_final_obj = data_final_obj - timedelta(days=1)
    
    dataFinal_corrigida_str = data_final_obj.isoformat()

    semana_do_ano = data_inicial_obj.isocalendar()[1]
    dia_da_semana = data_inicial_obj.isoweekday()

    remetente = "brunosilvabliu@gmail.com"
    emails_raw = request.form.get('email')
    assunto = "Convite para o Evento"
    mensagem = (f"Olá, você foi convidado para o evento: {nomeEvento}, que ocorrerá de {data_inicial_obj.strftime('%d/%m/%Y')} até {data_final_obj.strftime('%d/%m/%Y')}. Descrição: {descricao}.")
    senha = "bajo zusc ygzw fyqz"
    if emails_raw:
        emails = [e.strip() for e in emails_raw.split(",") if e.strip()]
        if emails:
            msg = EmailMessage()
            msg['From'] = remetente
            msg['To'] = ", ".join(emails)
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

    cursor.execute("""
    INSERT INTO dados (nomeEvento, dataInicial, dataFinal, descricao, eventColor, imagem_url, usuario_id, semana_do_ano, dia_da_semana, repetir_anualmente, evento_tipo)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (nomeEvento, dataInicial_str, dataFinal_corrigida_str, descricao, eventColor, imagem_url, usuario_id, semana_do_ano, dia_da_semana, repetir, evento_tipo_str))
    
    if repetir:
        duracao_evento = data_final_obj - data_inicial_obj
        ano_base = data_inicial_obj.year
        for ano in range(ano_base + 1, ano_base + 10):
            data_ini_obj = datetime.fromisocalendar(ano, semana_do_ano, dia_da_semana)
            data_fim_obj = data_ini_obj + duracao_evento
            cursor.execute("""
                INSERT INTO dados (nomeEvento, dataInicial, dataFinal, descricao, eventColor, imagem_url, usuario_id, semana_do_ano, dia_da_semana, repetir_anualmente, evento_tipo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 1, %s)
            """, (nomeEvento, data_ini_obj.date(), data_fim_obj.date(), descricao, eventColor, imagem_url, usuario_id, semana_do_ano, dia_da_semana, evento_tipo_str))

    conexao.commit()
    conexao.close()
    return jsonify({'mensagem': 'Evento criado com sucesso'}), 201

# Rota PUT para atualizar um evento
@app.route('/datas/<int:event_id>', methods=['PUT'])
def atualizar_evento(event_id):
    if 'usuario_id' not in session or session.get('tipo_usuario') != 'admin':
        return jsonify({'erro': 'Não autorizado'}), 401
    usuario_id = session['usuario_id']
    nomeEvento = request.form.get('nomeEvento')
    dataInicial = request.form.get('dataInicial')
    dataFinal = request.form.get('dataFinal')
    descricao = request.form.get('descricao')
    eventColor = request.form.get('eventColor')
    evento_tipos = request.form.getlist('evento_tipo')

    # ==========================================================
    # ALTERAÇÃO: Validação de Visibilidade na Atualização
    # ==========================================================
    if not evento_tipos:
        return jsonify({'erro': 'É necessário manter ao menos uma opção de visibilidade.'}), 400
    # ==========================================================

    evento_tipo_str = ",".join(evento_tipos)
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
    cursor.execute("UPDATE dados SET nomeEvento = %s, dataInicial = %s, dataFinal = %s, descricao = %s, eventColor = %s, imagem_url = %s, usuario_id = %s, evento_tipo = %s WHERE id = %s", (nomeEvento, dataInicial, dataFinal, descricao, eventColor, imagem_url, usuario_id, evento_tipo_str, event_id))
    conexao.commit()
    conexao.close()
    return jsonify({'mensagem': 'Evento atualizado com sucesso'})

# Rota DELETE para excluir um evento
@app.route('/datas/<int:event_id>', methods=['DELETE'])
def deletar_evento(event_id):
    if 'usuario_id' not in session or session.get('tipo_usuario') != 'admin':
        return jsonify({'erro': 'Não autorizado'}), 401
    conexao = get_db_connection()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM dados WHERE id = %s", (event_id,))
    conexao.commit()
    conexao.close()
    return jsonify({'mensagem': 'Evento excluído com sucesso'})
    
# Rota para iniciar a autenticação com o Google
@app.route('/google-login')
def google_login():
    client_config = {"web": {"client_id": os.getenv("GOOGLE_CLIENT_ID"), "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"), "auth_uri": "https://accounts.google.com/o/oauth2/auth", "token_uri": "https://oauth2.googleapis.com/token", "redirect_uris": ["http://localhost:5000/google-callback"]}}
    flow = google_auth_oauthlib.flow.Flow.from_client_config(client_config, scopes=SCOPES)
    flow.redirect_uri = url_for('google_callback', _external=True)
    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    session['state'] = state
    return redirect(authorization_url)

# Rota de callback do Google
@app.route('/google-callback')
def google_callback():
    state = session['state']
    client_config = {"web": {"client_id": os.getenv("GOOGLE_CLIENT_ID"), "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"), "auth_uri": "https://accounts.google.com/o/oauth2/auth", "token_uri": "https://oauth2.googleapis.com/token", "redirect_uris": ["http://localhost:5000/google-callback"]}}
    flow = google_auth_oauthlib.flow.Flow.from_client_config(client_config, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('google_callback', _external=True)
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    session['google_credentials'] = {'token': credentials.token, 'refresh_token': credentials.refresh_token, 'token_uri': credentials.token_uri, 'client_id': credentials.client_id, 'client_secret': credentials.client_secret, 'scopes': credentials.scopes}
    return redirect(url_for('import_google_calendar'))

# ROTA PARA IMPORTAR OS EVENTOS DO GOOGLE AGENDA
@app.route('/import-google-calendar')
def import_google_calendar():
    if 'google_credentials' not in session: return redirect(url_for('google_login'))
    if 'usuario_id' not in session: return redirect(url_for('login'))

    credentials = google.oauth2.credentials.Credentials(**session['google_credentials'])
    try:
        service = build('calendar', 'v3', credentials=credentials)
        now = datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(calendarId='primary', timeMin=now, singleEvents=True, orderBy='startTime').execute()
        google_events = events_result.get('items', [])

        if not google_events: return redirect(url_for('calendario_page'))

        conexao = get_db_connection()
        cursor = conexao.cursor()
        current_user_id = session['usuario_id']

        delete_sql = "DELETE FROM dados WHERE usuario_id = %s AND google_event_id IS NOT NULL"
        cursor.execute(delete_sql, (current_user_id,))

        processed_recurring_ids = set()
        for event in google_events:
            is_recurring = 'recurringEventId' in event
            if is_recurring:
                recurring_id = event['recurringEventId']
                if recurring_id in processed_recurring_ids:
                    continue
                processed_recurring_ids.add(recurring_id)

            start_str = event['start'].get('dateTime', event['start'].get('date'))
            end_str = event['end'].get('dateTime', event['end'].get('date'))
            
            data_inicial_obj = date.fromisoformat(start_str[:10])
            data_final_obj = date.fromisoformat(end_str[:10])
            if data_final_obj > data_inicial_obj:
                data_final_obj = data_final_obj - timedelta(days=1)

            nomeEvento = event.get('summary', 'Evento do Google')
            descricao = event.get('description', '')
            google_id = event['id']
            semana_do_ano = data_inicial_obj.isocalendar()[1]
            dia_da_semana = data_inicial_obj.isoweekday()
            
            cursor.execute("""
                INSERT INTO dados (nomeEvento, dataInicial, dataFinal, descricao, eventColor, usuario_id, google_event_id, semana_do_ano, dia_da_semana, repetir_anualmente, evento_tipo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (nomeEvento, data_inicial_obj, data_final_obj, descricao, None, current_user_id, google_id, semana_do_ano, dia_da_semana, is_recurring, 'admin'))

            if is_recurring:
                duracao_evento = data_final_obj - data_inicial_obj
                ano_base = data_inicial_obj.year
                for ano in range(ano_base + 1, ano_base + 10):
                    nova_data_ini_obj = datetime.fromisocalendar(ano, semana_do_ano, dia_da_semana)
                    nova_data_fim_obj = nova_data_ini_obj + duracao_evento
                    cursor.execute("""
                        INSERT INTO dados (nomeEvento, dataInicial, dataFinal, descricao, eventColor, usuario_id, google_event_id, semana_do_ano, dia_da_semana, repetir_anualmente, evento_tipo)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 1, %s)
                    """, (nomeEvento, nova_data_ini_obj.date(), nova_data_fim_obj.date(), descricao, None, current_user_id, google_id, semana_do_ano, dia_da_semana, 'admin'))
        
        conexao.commit()
        cursor.close()
        conexao.close()
        return redirect(url_for('calendario_page'))

    except HttpError as error:
        print(f'Ocorreu um erro: {error}')
        return "Ocorreu um erro ao buscar os eventos do Google Agenda.", 500
    except Exception as e:
        print(f"Erro Inesperado na importação: {e}")
        return "Ocorreu um erro inesperado durante a importação.", 500


# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)