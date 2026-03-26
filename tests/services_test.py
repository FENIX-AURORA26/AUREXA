import unittest
from unittest.mock import Mock, patch

import requests

from services.ai import responder
from services.license import verificar_licenca


class ResponderTests(unittest.TestCase):
    def test_responde_lentidao(self):
        self.assertIn("sobrecarregado", responder("Meu pc esta lento"))

    def test_resposta_padrao(self):
        self.assertIn("AUREXA", responder("ola"))


class VerificarLicencaTests(unittest.TestCase):
    def test_owner_tem_acesso_admin(self):
        self.assertEqual(verificar_licenca("AUREXA-OWNER-777"), "admin")

    @patch("services.license.requests.post")
    def test_usuario_valido_retorna_user(self, post_mock):
        resposta = Mock()
        resposta.json.return_value = {"status": "ok"}
        resposta.raise_for_status.return_value = None
        post_mock.return_value = resposta

        self.assertEqual(verificar_licenca("CLIENTE-001"), "user")

    @patch("services.license.requests.post")
    def test_erro_de_rede_retorna_none(self, post_mock):
        post_mock.side_effect = requests.RequestException("falha")

        self.assertIsNone(verificar_licenca("CLIENTE-001"))
