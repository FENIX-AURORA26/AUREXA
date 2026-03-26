# KVP_STUDIO (base AUREXA_BOREAL)

Plataforma desktop + console + API para voce criar, empacotar, instalar e monetizar apps com sua marca KVP, sem depender de terceiros.

## Dados principais que voce pediu

- Owner principal: `karollyne.pinheiro@fenix-boreal.com.br`
- Conta operacional adicional: `luna_site@fenix-boreal.com.br`
- API remota: `https://aurexa-api.onrender.com`
- Marca dos produtos: **KVP**
- Objetivo: criar programas/apps, gerar instalador e construir renda recorrente com planos

## Plataformas suportadas

- **Windows**: interface PyQt5 + instalador Inno Setup
- **Linux**: modo console + pacote portatil (`tar.gz`) + guia para `.deb`
- **macOS**: modo console (base atual), podendo evoluir para app bundle depois

## Instalacao

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
pip install -r requirements.txt
```

## Variaveis de ambiente

```text
AUREXA_API_BASE_URL=https://aurexa-api.onrender.com
AUREXA_LOCAL_API_BASE_URL=http://127.0.0.1:5000
AUREXA_OWNER_EMAIL=karollyne.pinheiro@fenix-boreal.com.br
AUREXA_OWNER_PASSWORD=
AUREXA_SUPPORT_TARGET=karollyne.pinheiro@fenix-boreal.com.br
AUREXA_SUPPORT_EMAIL=
AUREXA_SUPPORT_PASSWORD=
```

## Execucao

Interface grafica (Windows):

```powershell
.venv\Scripts\python.exe app_main.py
```

Modo automatico por sistema (Windows/Linux/macOS):

```bash
python run.py
```

API local:

```bash
python server.py
```

## Contas iniciais

- Owner: `karollyne.pinheiro@fenix-boreal.com.br` / `KvpStudio@2026`
- Free: `free@fenix-boreal.com.br` / `free123`
- Premium: `premium@fenix-boreal.com.br` / `premium123`
- Pro: `pro@fenix-boreal.com.br` / `pro123`

## Build e instaladores

### Windows

```powershell
.\build_release.ps1
```

Saida esperada:
- `dist/KVP_STUDIO.exe`
- `installer_output/KVP_STUDIO_Setup.exe` (quando Inno Setup estiver instalado)

### Linux

```bash
./build_release_linux.sh
```

Saida esperada:
- `installer_output/KVP_STUDIO_linux_portable.tar.gz`

Mais detalhes em `installer/linux/README.md`.

## Workspace de criacao de apps

- Use `studio/` para criar seus novos apps/produtos.
- Use a API para login/licenca/assinatura.
- Gere instaladores com marca KVP e publique para venda.

## Estrutura

- `app_main.py`: app desktop
- `console_main.py`: modo terminal
- `run.py`: entrada automatica por plataforma
- `server.py`: API local (login/licenca/planos)
- `build_release.ps1`: build/instalador Windows
- `build_release_linux.sh`: build/pacote Linux
- `installer/linux/`: material para distribuicao Linux
- `studio/`: espaco para criar novos apps/produtos




## Geração de apps por plataforma

### Windows 11 (EXE + Setup)
```powershell
.\build_release.ps1
```

### Arch Linux (PKGBUILD)
```bash
./build_archlinux.sh
# depois: cd installer_output/archlinux && makepkg -si
```

### macOS (.app / .dmg)
```bash
./build_macos.sh
```
> Precisa rodar em um Mac real.

### Android (APK/AAB - guia)
```bash
./build_android.sh
```
> Este projeto desktop usa PyQt5; para Android e recomendado app mobile dedicado consumindo a mesma API.

## Guia passo a passo (sem erros)

Para instalar no Windows, Linux, outras maquinas e distribuir para outras pessoas,
use o guia completo em `docs/INSTALL_GUIDE.md`.

Scripts de apoio:
- Windows: `setup_venv.ps1`
- Linux/macOS: `setup_venv.sh`


## Site Cyberpunk + Matrix

Novo site visual foi adicionado em `web/` com rota:
- `http://localhost:5000/landing`

Rodando localmente:
```bash
python server.py
```

## Servidor próprio (Docker)

```bash
docker compose up -d --build
```

Depois acesse:
- API health: `http://localhost:5000/health`
- Site: `http://localhost:5000/landing`


## Erro de conexão recusada (WinError 10061 / Connection refused)

Se aparecer "a máquina de destino recusou ativamente", faça nesta ordem:

1. Inicie API local:
```bash
python server.py
```
2. Teste saúde da API:
```bash
curl http://127.0.0.1:5000/health
```
3. Confirme variáveis:
- `AUREXA_API_BASE_URL`
- `AUREXA_LOCAL_API_BASE_URL=http://127.0.0.1:5000`

O app agora também tenta subir a API local automaticamente quando detecta falha de conexão na URL local.


### Caso apareca `ModuleNotFoundError: No module named 'flask'`

Instale as dependencias no mesmo Python que executa o app:

```powershell
python -m pip install -r requirements.txt
```

### Teste no PowerShell (sem erro de alias do curl)

No PowerShell, prefira:

```powershell
Invoke-WebRequest http://127.0.0.1:5000/health
```

ou:

```powershell
python -c "import requests; print(requests.get('http://127.0.0.1:5000/health').text)"
```


### Caso apareca status 400/401 no login

Isso normalmente e credencial ou licenca invalida.
Agora o app mostra a mensagem real da API (ex.: "Email ou senha invalidos") em vez de erro generico.

Checklist:
1. Email/senha corretos
2. Licenca correta para o email
3. Se necessario, use "Corrigir conexao" e tente novamente


## Novas funcoes de otimizacao (Windows e Linux)

- Limpar Cache (temporarios + DNS no Windows)
- Liberar RAM (coleta + diagnostico)
- Otimizar Processos (top CPU para voce finalizar o que pesa)
- Modo Turbo (cache + RAM + plano alto desempenho no Windows)

Essas funcoes estao na GUI e no modo console.


## Perfil Admin flexivel (trocar nome/email/senha)

No painel principal agora voce pode atualizar:
- nome
- email de login
- senha

Basta informar a senha atual e salvar. Isso remove dependencia de conta fixa "Luna" e permite entrar com outros emails admin do seu controle.

## IA e Painel Avancado

- IA com comandos para jogo/FPS, startup, RAM, travamento e modo ultra mega.
- Painel visual maior com botoes grandes e foco em uso real para PC novo e antigo.
- Modo Ultra Mega para diagnostico/otimizacao completa da maquina.


## IA estilo Chat + Modo Desenvolvedor

No painel existe alternancia de modo da IA:
- IA: Modo Normal
- IA: Modo Desenvolvedor

O modo desenvolvedor responde com foco em arquitetura, API, build, deploy e criacao de apps.

## Modo Gamer

- Botao dedicado **Modo Gamer** no painel.
- Ajusta rotina para jogos (limpeza, RAM, processos e perfil de desempenho).
- Ajuda a reduzir travamentos e queda de FPS.

## Dev Area completa

Veja `studio/DEV_AREA.md` e use:

```bash
python studio/tools/create_project.py
```

para criar novos projetos de app/programa rapidamente.


## Dev Console integrado na interface

Agora o painel principal tem um Dev Console com:
- Criar Projeto (gera app base em `studio/`)
- Build SO Atual (executa script de build conforme Windows/Linux/macOS)
- Checklist Publicacao

Isso aproxima o fluxo de um "ChatGPT + PC Manager + Studio" dentro do app.


## Terminal Dev embutido

No painel principal agora voce tem um terminal integrado para executar comandos de desenvolvimento,
como testes, build e scripts internos, com saida exibida na interface.


## Dev Terminal profissional (historico + stop)

No Terminal Dev embutido agora existe:
- Historico de comandos
- Botao para interromper comando em execucao
- Build por alvo: Windows, Linux, macOS, Arch e Android


## Layout IDE no Dev Console

O Dev Console agora possui abas dedicadas:
- Logs
- Build
- Terminal
- Templates

Com isso a experiencia fica mais profissional e organizada para desenvolvimento/publicacao.


## Atalhos do Dev Terminal

- **Ctrl+Enter**: Executar comando
- **Ctrl+L**: Limpar terminal
- **Ctrl+K**: Abrir historico

## Distribuicao para qualquer sistema/dispositivo

Use **Gerar Pacote Universal** no Dev Console para criar `installer_output/universal/README_INSTALL.txt`
com instrucoes centralizadas de instalacao para Windows/Linux/macOS/Android.


## Conectar no celular e outros dispositivos

1. Rode servidor local:
```bash
python server.py
```
2. Descubra URL para dispositivos na mesma rede:
```bash
http://SEU_IP_LOCAL:5000/server/device-connect-info
```
3. No celular, abra uma URL listada em `urls` e teste `.../health`.
4. Se nao abrir, libere porta 5000 no firewall.


## Dashboard Admin Web (/dashboard)

Novo painel admin web com cards e atualizacao em tempo real:
- usuarios totais
- usuarios online
- dispositivos conectados
- tabela completa de usuarios

Rotas:
- `/dashboard`
- `/server/dashboard-data`
