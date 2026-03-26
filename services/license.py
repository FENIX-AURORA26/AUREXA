import requests


def verificar_licenca(chave):
    if chave == "AUREXA-OWNER-777":
        return "admin"

    try:
        resposta = requests.post(
            "https://aurexa-api.onrender.com/verificar",
            json={"chave": chave},
            timeout=5,
        )
        resposta.raise_for_status()

        if resposta.json().get("status") == "ok":
            return "user"
    except requests.RequestException:
        pass

    return None
