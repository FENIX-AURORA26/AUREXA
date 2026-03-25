import platform
import os

sistema = platform.system()

if sistema == "Linux":
    print("Modo console")
    os.system("python console_main.py")
else:
    print("Modo interface")
    os.system("python app_main.py")