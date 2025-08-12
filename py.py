def ia_simples(pergunta):
    pergunta = pergunta.lower()
    
    if "olá" in pergunta or "ola" in pergunta or "oi" in pergunta or "eai" in pergunta or "e ai" in pergunta:
        return "Olá! Como posso te ajudar?"
    elif "tudo bem" in pergunta:
        return "Tudo ótimo, obrigado por perguntar!"
    elif "qual seu nome" in pergunta:
        return "Sou uma IA simples criada em Python."
    else:
        return "Desculpe, ainda não sei responder isso."

# Teste
while True:
    pergunta = input("Você: ")
    if pergunta.lower() in ['sair', 'exit']:
        break
    resposta = ia_simples(pergunta)
    print("IA:", resposta)
