import unittest
from unittest.mock import Mock, patch

from services.ai import responder
from services.api_client import ApiClient
from services.api_client import ApiClientError
from services.license import verificar_licenca
from services.local_store import get_plans, get_user_by_email, verify_user


class ResponderTests(unittest.TestCase):
    def test_responde_lentidao(self):
        self.assertIn("sobrecarregado", responder("Meu pc esta lento"))

    def test_resposta_padrao(self):
        self.assertIn("AUREXA_BOREAL", responder("ola"))

    def test_owner_recebe_resposta_admin(self):
        self.assertIn("acesso total", responder("qual meu acesso", role="owner"))


class LocalStoreTests(unittest.TestCase):
    def test_owner_seed_existe(self):
        owner = get_user_by_email("luna_site@fenix-boreal.com.br")
        self.assertIsNotNone(owner)
        self.assertEqual(owner["role"], "owner")

    def test_plans_seed_existem(self):
        planos = get_plans()
        self.assertEqual({plano["id"] for plano in planos}, {"free", "premium", "pro"})

    def test_verify_user(self):
        user = verify_user("free@fenix-boreal.com.br", "free123")
        self.assertIsNotNone(user)
        self.assertEqual(user["plan"], "free")


class VerificarLicencaTests(unittest.TestCase):
    @patch.object(ApiClient, "verify_license")
    def test_owner_tem_acesso_admin(self, verify_mock):
        verify_mock.return_value = {"status": "ok", "role": "owner"}
        self.assertEqual(
            verificar_licenca("luna_site@fenix-boreal.com.br", "AUREXA-OWNER-777"),
            "admin",
        )

    @patch.object(ApiClient, "verify_license")
    def test_usuario_valido_retorna_user(self, verify_mock):
        verify_mock.return_value = {"status": "ok", "role": "user"}
        self.assertEqual(
            verificar_licenca("premium@fenix-boreal.com.br", "AUREXA-PREMIUM-001"),
            "user",
        )

    @patch.object(ApiClient, "verify_license")
    def test_erro_da_api_retorna_none(self, verify_mock):
        verify_mock.side_effect = ApiClientError("falha")
        self.assertIsNone(
            verificar_licenca("free@fenix-boreal.com.br", "AUREXA-FREE-001")
        )


class ApiClientTests(unittest.TestCase):
    @patch("services.api_client.requests.request")
    def test_list_plans_retorna_json(self, request_mock):
        resposta = Mock()
        resposta.status_code = 200
        resposta.json.return_value = {"plans": [{"id": "free"}]}
        request_mock.return_value = resposta

        client = ApiClient(base_urls=["http://127.0.0.1:5000"])
        self.assertEqual(client.list_plans()["plans"][0]["id"], "free")
