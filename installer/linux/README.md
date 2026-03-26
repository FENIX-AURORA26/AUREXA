# KVP_STUDIO no Linux

Este diretório contém o fluxo base para distribuição Linux.

## Opção 1 (rápida): portátil tar.gz

```bash
./build_release_linux.sh
```

Saída:
- `installer_output/KVP_STUDIO_linux_portable.tar.gz`

## Opção 2 (pacote .deb)

Você pode transformar o binário em `.deb` com `fpm`:

```bash
sudo apt-get install ruby ruby-dev build-essential
sudo gem install --no-document fpm
fpm -s dir -t deb -n kvp-studio -v 1.0.0 installer_output/linux/=/opt/kvp-studio
```

## Serviço da API no Linux

Exemplo de inicialização:

```bash
python server.py
```

Para produção, use `gunicorn` + `systemd` e configure:
- Owner: `karollyne.pinheiro@fenix-boreal.com.br`
- API remota: `https://aurexa-api.onrender.com`
