import platform

import requests

import config


class ApiClientError(Exception):
    pass


class ApiClient:
    def __init__(self, base_urls=None, timeout=6):
        self.base_urls = base_urls or [config.REMOTE_API_BASE_URL, config.LOCAL_API_BASE_URL]
        self.timeout = timeout

    def _request(self, method, endpoint, **kwargs):
        last_error = None

        for base_url in self.base_urls:
            url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
            try:
                response = requests.request(method, url, timeout=self.timeout, **kwargs)
                if response.status_code >= 400:
                    last_error = ApiClientError(
                        f"API respondeu com status {response.status_code} em {url}"
                    )
                    continue
                return response.json()
            except requests.RequestException as exc:
                last_error = exc

        raise ApiClientError(f"Nao foi possivel conectar a API: {last_error}")

    def login(self, email, password):
        return self._request(
            "POST",
            "/auth/login",
            json={
                "email": email,
                "password": password,
                "device_name": platform.node() or config.APP_NAME,
                "platform": platform.system(),
            },
        )

    def verify_license(self, email, license_key):
        return self._request(
            "POST",
            "/licenses/verify",
            json={"email": email, "license_key": license_key},
        )

    def list_plans(self):
        return self._request("GET", "/plans")

    def list_licenses(self, email):
        return self._request("GET", "/licenses", params={"email": email})