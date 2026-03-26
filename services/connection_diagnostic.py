import subprocess
import sys
import time
from pathlib import Path

import requests

from config import LOCAL_API_BASE_URL


def _health_url(base_url=None):
    base = (base_url or LOCAL_API_BASE_URL).rstrip("/")
    return f"{base}/health"


def _api_online(base_url=None, timeout=2):
    try:
        response = requests.get(_health_url(base_url), timeout=timeout)
        return response.status_code == 200
    except requests.RequestException:
        return False


def _install_requirements():
    repo_root = Path(__file__).resolve().parent.parent
    req = repo_root / "requirements.txt"
    if req.exists():
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(req)])
    else:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])


def _ensure_flask_installed():
    try:
        import flask  # noqa: F401

        return True, "Flask OK"
    except Exception:
        try:
            _install_requirements()
            return True, "Dependencias instaladas com sucesso"
        except Exception as exc:
            return False, f"Falha ao instalar dependencias: {exc}"


def _start_local_server():
    repo_root = Path(__file__).resolve().parent.parent
    server_path = repo_root / "server.py"
    subprocess.Popen(  # noqa: S603,S607
        [sys.executable, str(server_path)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def diagnosticar_e_corrigir_api(base_url=None):
    logs = []

    flask_ok, flask_msg = _ensure_flask_installed()
    logs.append(flask_msg)
    if not flask_ok:
        return {"status": "error", "message": " | ".join(logs)}

    if _api_online(base_url=base_url):
        logs.append("API local ja estava online")
        return {"status": "ok", "message": " | ".join(logs)}

    logs.append("API offline: iniciando server.py")
    _start_local_server()

    for _ in range(5):
        time.sleep(1)
        if _api_online(base_url=base_url):
            logs.append("API local online apos correcao")
            return {"status": "ok", "message": " | ".join(logs)}

    logs.append("API continuou offline")
    return {"status": "error", "message": " | ".join(logs)}
