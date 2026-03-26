import unittest
from unittest.mock import patch

from services.connection_diagnostic import diagnosticar_e_corrigir_api


class ConnectionDiagnosticTests(unittest.TestCase):
    @patch("services.connection_diagnostic._api_online")
    @patch("services.connection_diagnostic._start_local_server")
    @patch("services.connection_diagnostic._ensure_flask_installed")
    def test_corrige_api_quando_offline(self, flask_mock, start_mock, online_mock):
        flask_mock.return_value = (True, "Flask OK")
        online_mock.side_effect = [False, True]

        resultado = diagnosticar_e_corrigir_api()

        self.assertEqual(resultado["status"], "ok")
        start_mock.assert_called_once()

    @patch("services.connection_diagnostic._ensure_flask_installed")
    def test_falha_se_dependencias_nao_instalam(self, flask_mock):
        flask_mock.return_value = (False, "Falha")

        resultado = diagnosticar_e_corrigir_api()

        self.assertEqual(resultado["status"], "error")
