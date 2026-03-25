def responder(pergunta):
    pergunta = pergunta.lower()

    if "lento" in pergunta:
        return "Seu sistema pode estar sobrecarregado. Use limpeza e modo turbo."

    elif "otimizar" in pergunta:
        return "Recomendo limpar cache e liberar RAM."

    elif "erro" in pergunta:
        return "Verifique logs ou reinicie o sistema."

    else:
        return "Sou a IA da AUREXA. Posso ajudar com desempenho."