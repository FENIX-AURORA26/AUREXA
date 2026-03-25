def responder(pergunta):
    pergunta = pergunta.lower()

    if "otimizar" in pergunta:
        return "Recomendo limpar cache e liberar RAM."

    elif "lento" in pergunta:
        return "Ative o modo turbo e feche processos."

    elif "erro" in pergunta:
        return "Verifique logs ou reinicie o sistema."

    else:
        return "Sou a IA da AUREXA. Posso ajudar com desempenho."