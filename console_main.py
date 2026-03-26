from config import APP_NAME
from core.optimizer import (
    analisar_inicializacao,
    liberar_ram,
    limpar_cache,
    modo_gamer,
    modo_turbo,
    modo_ultra_mega,
    otimizar_processos,
)


def main():
    while True:
        print(f"\n{APP_NAME} CONSOLE")
        print("1 - Limpar Cache")
        print("2 - Liberar RAM")
        print("3 - Otimizar Processos")
        print("4 - Modo Turbo")
        print("5 - Analisar Inicializacao")
        print("6 - Modo Ultra Mega")
        print("7 - Modo Gamer")
        print("0 - Sair")

        op = input("Escolha: ")

        if op == "1":
            print(limpar_cache())
        elif op == "2":
            print(liberar_ram())
        elif op == "3":
            print(otimizar_processos())
        elif op == "4":
            print(modo_turbo())
        elif op == "5":
            print(analisar_inicializacao())
        elif op == "6":
            print(modo_ultra_mega())
        elif op == "7":
            print(modo_gamer())
        elif op == "0":
            break


if __name__ == "__main__":
    main()
