import unittest
from pathlib import Path
from unittest.mock import patch

from services.dev_console import (
    build_alvo,
    checklist_publicacao,
    criar_projeto,
    executar_comando_terminal,
    gerar_pacote_universal,
    listar_historico,
)


class DevConsoleTests(unittest.TestCase):
    def test_checklist_publicacao_tem_itens(self):
        checklist = checklist_publicacao()
        self.assertIn("Checklist de publicacao", checklist)
        self.assertIn("Rodar testes", checklist)

    def test_criar_projeto(self):
        nome = "teste_dev_console"
        msg = criar_projeto(nome)
        self.assertIn("Projeto criado", msg)

        project_path = Path(__file__).resolve().parent.parent / "studio" / nome
        self.assertTrue((project_path / "README.md").exists())
        self.assertTrue((project_path / "main.py").exists())

    def test_executar_comando_terminal(self):
        saida = executar_comando_terminal("python -c \"print('ok_dev_terminal')\"")
        self.assertIn("ok_dev_terminal", saida)

    @patch("services.dev_console._run_script")
    def test_build_alvo_linux(self, run_mock):
        run_mock.return_value = "ok"
        resp = build_alvo("linux")
        self.assertEqual(resp, "ok")

    def test_historico_tem_comando(self):
        executar_comando_terminal("python -c \"print('hist_dev')\"")
        historico = listar_historico()
        self.assertIn("python -c", historico)


if __name__ == "__main__":
    unittest.main()
