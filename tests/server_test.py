import unittest

from server import app


class ServerTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health_endpoint(self):
        resposta = self.client.get("/health")
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json()["status"], "ok")

    def test_home_tem_links(self):
        resposta = self.client.get("/")
        self.assertEqual(resposta.status_code, 200)
        payload = resposta.get_json()
        self.assertEqual(payload["app"], "KVP_STUDIO")
        self.assertIn("quick_links", payload)

    def test_login_owner(self):
        resposta = self.client.post(
            "/auth/login",
            json={
                "email": "karollyne.pinheiro@fenix-boreal.com.br",
                "password": "KvpStudio@2026",
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
                "license_key": "KVP-PREMIUM-001",
            },
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json()["status"], "ok")

    def test_update_user_profile_invalid_password(self):
        resposta = self.client.post(
            "/users/update",
            json={
                "email": "karollyne.pinheiro@fenix-boreal.com.br",
                "current_password": "senha-errada",
                "new_name": "Novo Nome",
            },
        )
        self.assertEqual(resposta.status_code, 400)
        self.assertEqual(resposta.get_json()["status"], "error")

    def test_server_stats(self):
        resposta = self.client.get("/server/stats")
        self.assertEqual(resposta.status_code, 200)
        payload = resposta.get_json()
        self.assertEqual(payload["status"], "ok")
        self.assertIn("stats", payload)

    def test_device_connect_info(self):
        resposta = self.client.get("/server/device-connect-info")
        self.assertEqual(resposta.status_code, 200)
        payload = resposta.get_json()
        self.assertEqual(payload["status"], "ok")
        self.assertIn("urls", payload)


    def test_dashboard_data(self):
        resposta = self.client.get("/server/dashboard-data")
        self.assertEqual(resposta.status_code, 200)
        payload = resposta.get_json()
        self.assertEqual(payload["status"], "ok")
        self.assertIn("data", payload)
        self.assertIn("plan_breakdown", payload["data"])
        self.assertIn("platform_breakdown", payload["data"])
        self.assertIn("alerts", payload["data"])

    def test_dashboard_page(self):
        resposta = self.client.get("/dashboard")
        self.assertEqual(resposta.status_code, 200)
