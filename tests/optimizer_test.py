import unittest
from pathlib import Path
from unittest.mock import patch

from core.optimizer import modo_gamer, modo_turbo, otimizar_processos


class OptimizerTests(unittest.TestCase):
    @patch("core.optimizer._run")
    @patch("core.optimizer.platform.system")
    def test_otimizar_processos_windows(self, system_mock, run_mock):
        system_mock.return_value = "Windows"
        run_mock.return_value = (True, "chrome 123")

        msg = otimizar_processos()

        self.assertIn("Top processos", msg)
        self.assertIn("chrome", msg)

    @patch("core.optimizer._run")
    @patch("core.optimizer._remove_files_in_dir")
    @patch("core.optimizer.platform.system")
    def test_modo_turbo_windows(self, system_mock, remove_mock, run_mock):
        system_mock.return_value = "Windows"
        remove_mock.return_value = 3

        def side_effect(cmd):
            if cmd[:2] == ["ipconfig", "/flushdns"]:
                return True, "ok"
            if cmd[:2] == ["powercfg", "/setactive"]:
                return True, "ok"
            return True, "ok"

        run_mock.side_effect = side_effect

        msg = modo_turbo()

        self.assertIn("Cache limpo", msg)
        self.assertIn("Plano de energia", msg)


    @patch("core.optimizer._run")
    @patch("core.optimizer._remove_files_in_dir")
    @patch("core.optimizer.platform.system")
    def test_modo_gamer_windows(self, system_mock, remove_mock, run_mock):
        system_mock.return_value = "Windows"
        remove_mock.return_value = 1
        run_mock.return_value = (True, "ok")

        msg = modo_gamer()
        self.assertIn("MODO GAMER", msg)


if __name__ == "__main__":
    unittest.main()
