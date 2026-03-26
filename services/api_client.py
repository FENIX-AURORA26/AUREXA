import platform
import subprocess
import sys
import time
from pathlib import Path

import requests

from config import APP_NAME, LOCAL_API_BASE_URL, REMOTE_API_BASE_URL


class ApiClientError(Exception):
    pass


class ApiClient:
    def __init__(self, base_urls=None, timeout=6):
        self.base_urls = base_urls or [REMOTE_API_BASE_URL, LOCAL_API_BASE_URL]
        self.timeout = timeout
        self._local_api_bootstrapped = False

    def _is_local_base(self, base_url):
        normalized = base_url.lower()
        return "127.0.0.1" in normalized or "localhost" in normalized

    def _start_local_api(self):
        if self._local_api_bootstrapped:
            return

        server_path = Path(__file__).resolve().parent.parent / "server.py"
        if not server_path.exists():
            return

        subprocess.Popen(  # noqa: S603,S607
            [sys.executable, str(server_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        self._local_api_bootstrapped = True
        time.sleep(1.0)

    def _parse_error_payload(self, response):
        try:
            payload = response.json()
            if isinstance(payload, dict):
                return payload
        except ValueError:
            return None
        return None

    def _request(self, method, endpoint, allow_error_statuses=None, **kwargs):
        last_error = None
        allow_error_statuses = set(allow_error_statuses or [])

        for base_url in self.base_urls:
            url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
            try:
                response = requests.request(method, url, timeout=self.timeout, **kwargs)

                if response.status_code >= 400:
                    payload = self._parse_error_payload(response)
                    if response.status_code in allow_error_statuses and payload:
                        return payload

                    msg = payload.get("message") if isinstance(payload, dict) else None
                    if msg:
                        last_error = ApiClientError(
                            f"API respondeu com status {response.status_code} em {url}: {msg}"
                        )
                    else:
                        last_error = ApiClientError(
                            f"API respondeu com status {response.status_code} em {url}"
                        )
                    continue

                return response.json()
            except requests.RequestException as exc:
                last_error = exc

                if self._is_local_base(base_url) and not self._local_api_bootstrapped:
                    self._start_local_api()
                    try:
                        response = requests.request(method, url, timeout=self.timeout, **kwargs)
                        if response.status_code < 400:
                            return response.json()

                        payload = self._parse_error_payload(response)
                        if response.status_code in allow_error_statuses and payload:
                            return payload

                        msg = payload.get("message") if isinstance(payload, dict) else None
                        if msg:
                            last_error = ApiClientError(
                                f"API respondeu com status {response.status_code} em {url}: {msg}"
                            )
                        else:
                            last_error = ApiClientError(
                                f"API respondeu com status {response.status_code} em {url}"
                            )
                    except requests.RequestException as retry_exc:
                        last_error = retry_exc

        raise ApiClientError(
            "Nao foi possivel conectar a API. "
            f"Ultimo erro: {last_error}. "
            "Verifique internet, URL da API ou execute 'python server.py' para API local."
        )

    def login(self, email, password):
        return self._request(
            "POST",
            "/auth/login",
            allow_error_statuses={400, 401},
            json={
                "email": email,
                "password": password,
                "device_name": platform.node() or APP_NAME,
                "platform": platform.system(),
            },
        )

    def verify_license(self, email, license_key):
        return self._request(
            "POST",
            "/licenses/verify",
            allow_error_statuses={400},
            json={"email": email, "license_key": license_key},
        )

    def list_plans(self):
        return self._request("GET", "/plans")


    def update_profile(self, email, current_password, new_name=None, new_email=None, new_password=None):
        return self._request(
            "POST",
            "/users/update",
            allow_error_statuses={400},
            json={
                "email": email,
                "current_password": current_password,
                "new_name": new_name,
                "new_email": new_email,
                "new_password": new_password,
            },
        )
