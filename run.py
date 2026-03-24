import platform
import os

sistema = platform.system()

if sistema == "Linux":
    print("Modo console ativado")
    os.system("python console_main.py")
else:
    print("Modo interface ativado")
    os.system("python app_main.py")