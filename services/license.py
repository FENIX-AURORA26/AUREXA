from services.api_client import ApiClient, ApiClientError


def verificar_licenca(email, chave):
    client = ApiClient()

    try:
        resposta = client.verify_license(email, chave)
    except ApiClientError:
        return None

    if resposta.get("status") != "ok":
        return None
    if resposta.get("role") == "owner":
        return "admin"
    return "user"
