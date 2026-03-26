import platform
import subprocess
from pathlib import Path

_COMMAND_HISTORY = []


def _project_root():
    return Path(__file__).resolve().parent.parent


def registrar_historico(comando):
    comando = (comando or "").strip()
    if not comando:
        return
    _COMMAND_HISTORY.append(comando)
    del _COMMAND_HISTORY[:-50]


def listar_historico():
    if not _COMMAND_HISTORY:
        return "Sem historico de comandos ainda."
    return "\n".join(f"{idx+1}. {cmd}" for idx, cmd in enumerate(_COMMAND_HISTORY))


def criar_projeto(nome):
    nome = (nome or "novo_app").strip().replace(" ", "_")
    if not nome:
        nome = "novo_app"

    studio_root = _project_root() / "studio"
    target = studio_root / nome
    target.mkdir(parents=True, exist_ok=True)

    readme = f"# {nome}\n\nProjeto criado pelo Dev Console KVP_STUDIO.\n"
    main = (
        "def main():\n"
        f"    print(\"{nome} iniciado\")\n\n"
        "if __name__ == '__main__':\n"
        "    main()\n"
    )

    (target / "README.md").write_text(readme, encoding="utf-8")
    (target / "main.py").write_text(main, encoding="utf-8")

    return f"Projeto criado em: {target}"


def _run_script(script_name):
    root = _project_root()
    script_path = root / script_name
    if not script_path.exists():
        return f"Script nao encontrado: {script_name}"

    shell = ["bash", str(script_path)]
    if script_name.endswith(".ps1"):
        shell = ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(script_path)]

    try:
        result = subprocess.run(shell, capture_output=True, text=True, timeout=180)
        output = (result.stdout or result.stderr or "").strip()
        return f"[{script_name}] codigo={result.returncode}\n{output}"
    except Exception as exc:
        return f"Falha ao executar {script_name}: {exc}"


def build_os_atual():
    sistema = platform.system()

    if sistema == "Windows":
        return _run_script("build_release.ps1")
    if sistema == "Linux":
        return _run_script("build_release_linux.sh")
    if sistema == "Darwin":
        return _run_script("build_macos.sh")

    return f"Sistema {sistema} ainda sem build automatizado."


def build_alvo(alvo):
    alvo = (alvo or "").strip().lower()
    scripts = {
        "windows": "build_release.ps1",
        "linux": "build_release_linux.sh",
        "macos": "build_macos.sh",
        "arch": "build_archlinux.sh",
        "android": "build_android.sh",
    }
    script = scripts.get(alvo)
    if not script:
        return f"Alvo invalido: {alvo}"
    return _run_script(script)


def checklist_publicacao():
    return (
        "Checklist de publicacao:\n"
        "1) Rodar testes (python -m unittest discover -s tests -p '*test.py')\n"
        "2) Validar login e API /health\n"
        "3) Gerar build por sistema\n"
        "4) Testar instalacao em maquina limpa\n"
        "5) Publicar e monitorar erros"
    )


def executar_comando_terminal(comando, timeout=90):
    comando = (comando or "").strip()
    if not comando:
        return "Comando vazio."

    registrar_historico(comando)

    try:
        result = subprocess.run(
            comando,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=_project_root(),
        )
        saida = (result.stdout or "") + ("\n" + result.stderr if result.stderr else "")
        saida = saida.strip() or "(sem saida)"
        return f"$ {comando}\n[exit={result.returncode}]\n{saida}"
    except Exception as exc:
        return f"Falha ao executar comando: {exc}"



def gerar_pacote_universal():
    root = _project_root()
    out = root / "installer_output" / "universal"
    out.mkdir(parents=True, exist_ok=True)

    artefatos = [
        root / "installer_output" / "KVP_STUDIO_Setup.exe",
        root / "installer_output" / "KVP_STUDIO_linux_portable.tar.gz",
        root / "installer_output" / "macos" / "KVP_STUDIO_MAC.app",
    ]

    encontrados = []
    for art in artefatos:
        if art.exists():
            encontrados.append(str(art))

    guia = (
        "KVP_STUDIO - Pacote Universal de Distribuicao\n"
        "Sistemas alvo: Windows, Linux, macOS e Android (guia).\n\n"
        "Instalacao rapida:\n"
        "- Windows: execute KVP_STUDIO_Setup.exe\n"
        "- Linux: extraia KVP_STUDIO_linux_portable.tar.gz\n"
        "- macOS: abra KVP_STUDIO_MAC.app\n"
        "- Android: use build_android.sh para gerar APK/AAB no ambiente adequado\n\n"
        f"Artefatos encontrados: {len(encontrados)}\n" + "\n".join(encontrados)
    )

    (out / "README_INSTALL.txt").write_text(guia, encoding="utf-8")
    return f"Pacote universal preparado em: {out}"
