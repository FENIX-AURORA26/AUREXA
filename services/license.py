import requests

def verificar_licenca(chave):

    # 👑 DONA (ACESSO TOTAL)
    if chave == "AUREXA-OWNER-777":
        return "admin"

    # 🌐 VERIFICA ONLINE
    try:
        r = requests.post(
            "https://aurexa-api.onrender.com/verificar",
            json={"chave": chave},
            timeout=5
        )

        if r.json()["status"] == "ok":
            return "user"

    except:
        pass

    return None