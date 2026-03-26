import platform
import subprocess
import sys
from pathlib import Path

from config import APP_NAME


BASE_DIR = Path(__file__).resolve().parent


def main():
    sistema = platform.system()

    if sistema in {"Linux", "Darwin"}:
        print(f"Modo console {APP_NAME} ({sistema})")
        alvo = BASE_DIR / "console_main.py"
    else:
        print(f"Modo interface {APP_NAME} ({sistema})")
        alvo = BASE_DIR / "app_main.py"

    subprocess.run([sys.executable, str(alvo)], check=True)


if __name__ == "__main__":
    main()
