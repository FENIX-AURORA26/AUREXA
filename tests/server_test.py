import unittest

from server import app


class ServerTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health_endpoint(self):
        resposta = self.client.get("/health")
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json()["status"], "ok")

    def test_login_owner(self):
        resposta = self.client.post(
            "/auth/login",
            json={
                "email": "luna_site@fenix-boreal.com.br",
                "password": "AurexaBoreal@123",
                "device_name": "test-device",
                "platform": "Windows",
            },
        )
        self.assertEqual(resposta.status_code, 200)
        payload = resposta.get_json()
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["session"]["user"]["role"], "owner")

    def test_verify_license(self):
        resposta = self.client.post(
            "/licenses/verify",
            json={
                "email": "premium@fenix-boreal.com.br",
                "license_key": "AUREXA-PREMIUM-001",
            },
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json()["status"], "ok")
