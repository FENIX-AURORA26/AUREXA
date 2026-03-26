import os
import platform


def limpar_cache():
    sistema = platform.system()

    try:
        if sistema == "Windows":
            os.system("cleanmgr /sagerun:1")
        elif sistema == "Linux":
            os.system("sudo apt-get clean")
        return "Cache limpo com sucesso!"
    except Exception:
        return "Erro ao limpar cache"


def liberar_ram():
    sistema = platform.system()

    try:
        if sistema == "Linux":
            os.system("sync; echo 3 | sudo tee /proc/sys/vm/drop_caches")
            return "RAM liberada!"
        return "Funcao disponivel apenas no Linux"
    except Exception:
        return "Erro ao liberar RAM"
