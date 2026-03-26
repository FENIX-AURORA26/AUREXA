# AUREXA

Aplicacao desktop e console para utilitarios de sistema, login por licenca e recursos simples de suporte.

## Requisitos

- Python 3.11+ recomendado
- Windows para interface PyQt5
- Linux para modo console

## Instalacao

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Execucao

Interface grafica:

```powershell
.venv\Scripts\python.exe app_main.py
```

Modo automatico:

```powershell
.venv\Scripts\python.exe run.py
```

API local:

```powershell
.venv\Scripts\python.exe server.py
```

## Variaveis de ambiente

Para o envio de suporte por email:

```text
AUREXA_SUPPORT_EMAIL=
AUREXA_SUPPORT_PASSWORD=
```

Voce pode usar `.env.example` como referencia e configurar essas variaveis no sistema ou no terminal antes de rodar o app.

## Build

```powershell
.venv\Scripts\pyinstaller.exe app_main.spec
```

## Testes

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -p "*test.py"
```

## Estrutura

- `app_main.py`: entrada da interface grafica
- `console_main.py`: entrada do modo console
- `run.py`: seletor simples por sistema operacional
- `server.py`: API local de verificacao de licenca
- `ui/`: telas PyQt5
- `services/`: integracoes e servicos
- `core/`: utilitarios internos
