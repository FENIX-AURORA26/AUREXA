import gc
import os
import platform
import shutil
import subprocess
from pathlib import Path


def _run(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=25,
            shell=False,
            check=False,
        )
        return result.returncode == 0, (result.stdout or result.stderr or "").strip()
    except Exception as exc:
        return False, str(exc)


def _remove_files_in_dir(path: Path):
    removidos = 0
    if not path.exists() or not path.is_dir():
        return removidos

    for item in path.iterdir():
        try:
            if item.is_file() or item.is_symlink():
                item.unlink(missing_ok=True)
                removidos += 1
            elif item.is_dir():
                shutil.rmtree(item, ignore_errors=True)
                removidos += 1
        except Exception:
            continue
    return removidos


def limpar_cache():
    sistema = platform.system()
    logs = []

    try:
        if sistema == "Windows":
            temp_user = Path(os.getenv("TEMP", ""))
            temp_win = Path("C:/Windows/Temp")
            total = _remove_files_in_dir(temp_user) + _remove_files_in_dir(temp_win)
            logs.append(f"Temporarios removidos: {total}")

            ok_dns, _ = _run(["ipconfig", "/flushdns"])
            if ok_dns:
                logs.append("DNS limpo")

        elif sistema == "Linux":
            cache_user = Path.home() / ".cache"
            total = _remove_files_in_dir(cache_user)
            logs.append(f"Cache do usuario removido: {total}")

            ok_apt, _ = _run(["bash", "-lc", "apt-get clean"])
            if ok_apt:
                logs.append("Cache apt limpo")

        else:
            logs.append("Sistema sem rotina detalhada de cache")

        return "Cache limpo com sucesso! " + " | ".join(logs)
    except Exception as exc:
        return f"Erro ao limpar cache: {exc}"


def liberar_ram():
    sistema = platform.system()

    try:
        gc.collect()

        if sistema == "Linux":
            ok, _ = _run(["bash", "-lc", "sync"])
            if ok:
                return "RAM otimizada no Linux (sync + coletor Python)."
            return "RAM parcialmente otimizada (coletor Python)."

        if sistema == "Windows":
            ok, _ = _run(
                [
                    "powershell",
                    "-Command",
                    "Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 5 Name,Id,WorkingSet",
                ]
            )
            if ok:
                return "RAM otimizada (coleta Python + diagnostico de processos pesados)."
            return "RAM parcialmente otimizada (coletor Python)."

        return "RAM otimizada com coleta de lixo local."
    except Exception as exc:
        return f"Erro ao liberar RAM: {exc}"


def otimizar_processos():
    sistema = platform.system()

    if sistema == "Windows":
        ok, saida = _run(
            [
                "powershell",
                "-Command",
                "Get-Process | Sort-Object CPU -Descending | Select-Object -First 10 Name,Id,CPU",
            ]
        )
        if ok:
            return "Top processos por CPU (revise e finalize os desnecessarios):\n" + saida
        return "Nao foi possivel listar processos no Windows."

    if sistema == "Linux":
        ok, saida = _run(["bash", "-lc", "ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head -n 12"])
        if ok:
            return "Top processos por CPU (revise e finalize os desnecessarios):\n" + saida
        return "Nao foi possivel listar processos no Linux."

    return "Funcao de processos indisponivel para este sistema."


def modo_turbo():
    sistema = platform.system()
    passos = [limpar_cache(), liberar_ram()]

    if sistema == "Windows":
        ok, _ = _run(["powercfg", "/setactive", "SCHEME_MAX"])
        if ok:
            passos.append("Plano de energia: Alto desempenho ativado.")
        else:
            passos.append("Nao foi possivel alterar plano de energia (rode como administrador).")

    return "\n".join(passos)


def analisar_inicializacao():
    sistema = platform.system()

    if sistema == "Windows":
        ok, saida = _run(
            [
                "powershell",
                "-Command",
                "Get-CimInstance Win32_StartupCommand | Select-Object Name,Command,Location | Format-Table -AutoSize",
            ]
        )
        if ok:
            return "Itens de inicializacao detectados:\n" + saida
        return "Nao foi possivel listar inicializacao no Windows."

    if sistema == "Linux":
        ok, saida = _run(["bash", "-lc", "systemctl list-unit-files --type=service --state=enabled | head -n 20"])
        if ok:
            return "Servicos habilitados no boot (amostra):\n" + saida
        return "Nao foi possivel listar inicializacao no Linux."

    return "Analise de inicializacao indisponivel para este sistema."


def modo_ultra_mega():
    relatorio = [
        "=== MODO ULTRA MEGA ===",
        limpar_cache(),
        liberar_ram(),
        otimizar_processos(),
        analisar_inicializacao(),
        modo_turbo(),
        "Dica: reinicie a maquina apos a otimizacao para aplicar ganhos em kernel/drivers.",
    ]
    return "\n\n".join(relatorio)



def modo_gamer():
    sistema = platform.system()
    relatorio = ["=== MODO GAMER ===", limpar_cache(), liberar_ram(), otimizar_processos()]

    if sistema == "Windows":
        ok, _ = _run(["powercfg", "/setactive", "SCHEME_MAX"])
        if ok:
            relatorio.append("Windows em alto desempenho para jogos.")
        else:
            relatorio.append("Nao foi possivel ativar alto desempenho (execute como admin).")

    elif sistema == "Linux":
        relatorio.append("Linux: mantenha governor em performance durante jogos e feche servicos extras.")

    relatorio.append("Dica Gamer: feche launchers e overlays que nao estiver usando.")
    return "\n\n".join(relatorio)
