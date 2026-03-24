from core.optimizer import limpar_cache, liberar_ram

def menu():
    while True:
        print("\n=== AUREXA CORE ===")
        print("1 - Limpar Cache")
        print("2 - Liberar RAM")
        print("0 - Sair")

        escolha = input("Escolha: ")

        if escolha == "1":
            print(limpar_cache())

        elif escolha == "2":
            print(liberar_ram())

        elif escolha == "0":
            break

menu()