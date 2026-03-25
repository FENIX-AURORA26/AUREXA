from core.optimizer import limpar_cache, liberar_ram

while True:
    print("\nAUREXA CONSOLE")
    print("1 - Limpar Cache")
    print("2 - Liberar RAM")
    print("0 - Sair")

    op = input("Escolha: ")

    if op == "1":
        print(limpar_cache())
    elif op == "2":
        print(liberar_ram())
    elif op == "0":
        break