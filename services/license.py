def verificar_licenca(chave):
    # 👑 CHAVE MASTER (VOCÊ)
    if chave == "AUREXA-OWNER-777":
        return True

    import requests
    try:
        r = requests.post(
            "https://aurexa.onrender.com/verificar",
            json={"chave": chave}
        )
        return r.json()["status"] == "ok"
    except:
        return False