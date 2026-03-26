def responder(pergunta, plano="free", role="user", modo="normal"):
    pergunta = (pergunta or "").lower()

    if modo == "developer":
        if "api" in pergunta:
            return (
                "[DEV MODE] Sugestao de arquitetura: Flask API + camada services + testes unitarios + "
                "docker-compose para deploy. Posso gerar endpoints, contratos JSON e scripts de build."
            )
        if "app" in pergunta or "programa" in pergunta:
            return (
                "[DEV MODE] Fluxo recomendado: idea -> scaffold -> feature -> testes -> empacotamento "
                "(Windows/Linux/macOS) -> instalador -> metricas de uso."
            )
        return (
            "[DEV MODE] Estou em modo desenvolvedor avancado. Posso ajudar com codigo, arquitetura, "
            "refatoracao, debugging, build, deploy e performance."
        )

    if role == "owner":
        return (
            "Modo owner ativo. Voce tem acesso total ao KVP_STUDIO: usuarios, licencas, "
            "assinaturas, automacoes e painel de otimizacao avancada."
        )

    if "gamer" in pergunta or "jogo" in pergunta or "fps" in pergunta:
        return (
            "Use Modo Gamer: ativa perfil de desempenho, limpa processos pesados e melhora "
            "estabilidade para reduzir quedas de FPS."
        )
    if "ultra" in pergunta or "mega" in pergunta:
        return (
            "Use o Modo Ultra Mega: limpa cache, melhora RAM, analisa processos e ativa "
            "perfil de alto desempenho para reduzir travamentos."
        )
    if "startup" in pergunta or "inicializacao" in pergunta:
        return "Revise apps de inicializacao para reduzir uso de CPU e RAM no boot."
    if "lento" in pergunta or "travando" in pergunta:
        return "Seu sistema pode estar sobrecarregado. Rode limpeza de cache, diagnostico de processos e modo turbo agora."
    if "otimizar" in pergunta:
        return "Recomendo: Limpar Cache -> Liberar RAM -> Otimizar Processos -> Modo Ultra Mega."
    if "erro" in pergunta:
        return "Verifique logs locais, API e conexao. Se preciso, use o botao Corrigir Conexao."
    if "assinatura" in pergunta or "plano" in pergunta:
        return f"Seu plano atual e {plano}. Niveis: free, premium e pro."
    if "vender" in pergunta or "renda" in pergunta:
        return "Use plano pro, gere instaladores e acompanhe metricas para monetizacao."

    return "Sou a IA da KVP_STUDIO: desempenho, conta, monetizacao e suporte tecnico." 
