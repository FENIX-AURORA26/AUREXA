import platform
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def main():
    sistema = platform.system()

    if sistema == "Linux":
        print("Modo console")
        alvo = BASE_DIR / "console_main.py"
    else:
        print("Modo interface")
        alvo = BASE_DIR / "app_main.py"

    subprocess.run([sys.executable, str(alvo)], check=True)


if __name__ == "__main__":
    main()
