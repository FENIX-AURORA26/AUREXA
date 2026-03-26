# Guia de Instalação e Distribuição — KVP_STUDIO

Este guia é para:
1. **Você instalar e rodar** no seu Windows/Linux.
2. **Publicar para outras máquinas**.
3. **Entregar para outras pessoas instalarem**.

---

## 1) Instalação no Windows (desenvolvimento)

### Pré-requisitos
- Windows 10/11
- Python 3.11+
- PowerShell

### Passo a passo

1. Abra PowerShell na pasta do projeto.
2. Crie ambiente virtual:

```powershell
python -m venv .venv
```

3. Ative o ambiente:

```powershell
.venv\Scripts\activate
```

4. Instale dependências:

```powershell
pip install -r requirements.txt
```

5. (Opcional) Configure variáveis com base em `.env.example`.

6. Rode testes:

```powershell
python -m unittest discover -s tests -p "*test.py"
```

7. Abra o app (GUI):

```powershell
python app_main.py
```

8. Rode API local (quando necessário):

```powershell
python server.py
```

---

## 2) Instalação no Linux (desenvolvimento)

### Pré-requisitos
- Ubuntu/Debian/Fedora (ou similar)
- Python 3.11+
- `python3-venv`

### Passo a passo

1. Abra terminal na pasta do projeto.
2. Crie e ative ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instale dependências:

```bash
pip install -r requirements.txt
```

4. Rode testes:

```bash
python -m unittest discover -s tests -p '*test.py'
```

5. Rode modo automático (Linux usa console por padrão):

```bash
python run.py
```

6. Suba API local:

```bash
python server.py
```

---

## 3) Gerar instalador para outras pessoas (Windows)

### 3.1 Gerar EXE

```powershell
.\build_release.ps1
```

Saída mínima:
- `dist/KVP_STUDIO.exe`

### 3.2 Gerar Setup `.exe`
- Instale Inno Setup (iscc no PATH)
- Rode novamente:

```powershell
.\build_release.ps1
```

Saída final:
- `installer_output/KVP_STUDIO_Setup.exe`

Esse arquivo pode ser enviado para outras pessoas instalarem no Windows.

---

## 4) Gerar pacote para outras pessoas (Linux)

```bash
./build_release_linux.sh
```

Saída:
- `installer_output/KVP_STUDIO_linux_portable.tar.gz`

A pessoa que receber pode extrair e executar o binário `KVP_STUDIO`.

---

## 5) Instalar em outras máquinas da sua empresa

### Opção A: Sem build (código-fonte)
- Clone/copiar repositório
- Repetir passos de instalação Windows/Linux acima

### Opção B: Com build (recomendado para usuário final)
- Windows: enviar `KVP_STUDIO_Setup.exe`
- Linux: enviar `KVP_STUDIO_linux_portable.tar.gz`

---

## 6) Checklist “sem erros” antes de publicar

1. Testes verdes:
```bash
python -m unittest discover -s tests -p '*test.py'
```
2. API responde:
```bash
python server.py
# abrir /health
```
3. Login owner válido:
- Email: `karollyne.pinheiro@fenix-boreal.com.br`
4. Build gerado no sistema de destino (Windows/Linux).

---

## 7) Dados da sua operação

- Email principal: `karollyne.pinheiro@fenix-boreal.com.br`
- Email operacional: `luna_site@fenix-boreal.com.br`
- API remota: `https://aurexa-api.onrender.com`


## 8) Build por plataforma (pedido: Windows 11, Arch, Mac e Android)

### Windows 11
```powershell
.\build_release.ps1
```

### Arch Linux
```bash
./build_archlinux.sh
cd installer_output/archlinux
makepkg -si
```

### macOS
```bash
./build_macos.sh
```
> Rode em macOS para gerar `.app/.dmg`.

### Android
```bash
./build_android.sh
```
> Gera checklist/guia. Para APK/AAB real, montar app mobile dedicado integrado na mesma API.


## 9) Subir site + servidor próprio (Docker)

1. Instale Docker e Docker Compose.
2. Na pasta do projeto execute:

```bash
docker compose up -d --build
```

3. Acesse:
- Site cyberpunk/matrix: `http://localhost:5000/landing`
- API health: `http://localhost:5000/health`

4. Para parar:

```bash
docker compose down
```


## 10) Erro comum: `No module named flask`

Se isso acontecer, execute:

```bash
python -m pip install -r requirements.txt
```

No PowerShell, para testar API use:

```powershell
Invoke-WebRequest http://127.0.0.1:5000/health
```


## 11) Trocar nome/email/senha do admin

1. Entre no app.
2. No painel principal, use a area **Atualizar Perfil/Admin**.
3. Informe senha atual.
4. Informe novo nome/email/senha e salve.

## 12) Modo Ultra Mega (PCs antigos e novos)

No painel:
- clique em **Modo Ultra Mega** para executar limpeza + RAM + processos + startup + turbo.


## 13) IA Modo Desenvolvedor e Modo Gamer

No painel principal:
1. Clique em **IA: Modo Normal** para alternar para **Modo Desenvolvedor**.
2. Use perguntas sobre API, arquitetura, build e deploy.
3. Use **Modo Gamer** para perfil de jogo e otimização rápida.


## 14) Dev Console dentro do painel

No painel principal use:
1. **Criar Projeto** (gera estrutura base em `studio/`)
2. **Build SO Atual** (usa script do seu sistema)
3. **Checklist Publicacao** (passo a passo de release)


## 15) Terminal Dev embutido

No painel principal:
1. Digite comando no campo de terminal.
2. Clique em **Executar Comando**.
3. Veja a saida no bloco de terminal embutido.


## 16) Historico e Stop no Terminal Dev

No painel Dev Console:
1. Execute um comando no terminal embutido.
2. Use **Historico de Comandos** para rever comandos anteriores.
3. Use **Parar Comando** para interromper processos longos.
4. Use botões de **Build por alvo** para Windows/Linux/macOS/Arch/Android.


## 17) Abas IDE no Dev Console

No painel Dev Console voce encontra abas:
1. **Logs**: eventos e auditoria rapida
2. **Build**: build por SO/alvo
3. **Terminal**: comando com stop + historico
4. **Templates**: criacao de novos projetos


## 18) Atalhos rapidos do Terminal Dev

- Ctrl+Enter: executar comando
- Ctrl+L: limpar terminal
- Ctrl+K: abrir historico

## 19) Pacote Universal (qualquer sistema)

No Dev Console > Build, clique em **Gerar Pacote Universal**.
Isso cria `installer_output/universal/README_INSTALL.txt` com instrucoes para Windows/Linux/macOS/Android.


## 20) Conectar servidor no celular

1. Execute `python server.py` no computador.
2. Acesse `http://127.0.0.1:5000/server/device-connect-info` para ver URLs da rede local.
3. No celular (mesmo Wi-Fi), abra `http://SEU_IP:5000/health`.
4. Se falhar, ajuste firewall/roteador para liberar a porta 5000.


## 21) Dashboard admin em tempo real

1. Rode `python server.py`
2. Abra `http://SEU_IP:5000/dashboard`
3. O painel atualiza a cada 5 segundos consumindo `/server/dashboard-data`
