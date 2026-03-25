import requests

def verificar_licenca(chave):
    try:
        r = requests.post(
            "http://127.0.0.1:5000/verificar",
            json={"chave": chave}
        )
        return r.json()["status"] == "ok"
    except:
        return False