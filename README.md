# AUREXA_BOREAL

Aplicacao desktop e console com login por email e senha, licencas, planos de assinatura e API para Windows e Linux.

## Requisitos

- Python 3.11+ recomendado
- Windows para interface PyQt5
- Linux para modo console
- API local Flask ou API remota em `https://aurexa-api.onrender.com`

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

Para o envio de suporte e configuracao:

```text
AUREXA_API_BASE_URL=https://aurexa-api.onrender.com
AUREXA_LOCAL_API_BASE_URL=http://127.0.0.1:5000
AUREXA_OWNER_EMAIL=luna_site@fenix-boreal.com.br
AUREXA_OWNER_PASSWORD=
AUREXA_SUPPORT_TARGET=luna_site@fenix-boreal.com.br
AUREXA_SUPPORT_EMAIL=
AUREXA_SUPPORT_PASSWORD=
```

Voce pode usar `.env.example` como referencia e configurar essas variaveis no sistema ou no terminal antes de rodar o app.

## Contas iniciais de exemplo

- Owner: `luna_site@fenix-boreal.com.br`
- Free: `free@fenix-boreal.com.br` / `free123`
- Premium: `premium@fenix-boreal.com.br` / `premium123`
- Pro: `pro@fenix-boreal.com.br` / `pro123`

Altere a senha owner via variavel `AUREXA_OWNER_PASSWORD`.

## Build

```powershell
.venv\Scripts\pyinstaller.exe app_main.spec
```

Instalador Windows:

```powershell
.\build_release.ps1
```

Se o Inno Setup estiver instalado, o instalador final sera gerado em `installer_output\AUREXA_BOREAL_Setup.exe`.
Se nao estiver, o script ainda gera o executavel em `dist\AUREXA_BOREAL.exe` e mostra o comando para compilar o instalador depois.

## Testes

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -p "*test.py"
```

## Estrutura

- `app_main.py`: entrada da interface grafica
- `console_main.py`: entrada do modo console
- `run.py`: seletor simples por sistema operacional
- `server.py`: API local de login, planos e licencas
- `ui/`: telas PyQt5
- `services/`: integracoes e servicos
- `core/`: utilitarios internos
- `data/`: base local JSON para bootstrap
- `installer/`: script do instalador Windows com Inno Setup
- `branding/`: logos e guia visual do AUREXA_BOREAL
- `studio/`: espaco para seus futuros apps e templates

## Marca

Arquivos principais de identidade:

- `branding/AUREXA_BOREAL_logo.svg`
- `branding/AUREXA_BOREAL_wordmark.svg`
- `branding/BRAND_GUIDE.md`
