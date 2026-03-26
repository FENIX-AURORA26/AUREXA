def responder(pergunta, plano="free", role="user"):
    pergunta = pergunta.lower()

    if role == "owner":
        return (
            "Modo owner ativo. Voce tem acesso total ao AUREXA_BOREAL, incluindo "
            "gestao de usuarios, licencas e assinaturas."
        )

    if "lento" in pergunta:
        return "Seu sistema pode estar sobrecarregado. Use limpeza e modo turbo."
    if "otimizar" in pergunta:
        return "Recomendo limpar cache e liberar RAM."
    if "erro" in pergunta:
        return "Verifique logs ou reinicie o sistema."
    if "assinatura" in pergunta or "plano" in pergunta:
        return f"Seu plano atual e {plano}. Os niveis disponiveis sao free, premium e pro."

    return "Sou a IA da AUREXA_BOREAL. Posso ajudar com desempenho e conta."
