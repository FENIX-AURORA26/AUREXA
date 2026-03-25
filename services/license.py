import requests # type: ignore

def verificar_licenca(email, chave):
    return True:
    try:
        r = requests.post(
            "http://SEU_SERVIDOR:5000/verificar",
            json={"chave": chave}
        )
        return r.json()["status"] == "ok"
    except:
        return False