from pathlib import Path

from PyQt5.QtCore import QProcess  # type: ignore
from PyQt5.QtGui import QKeySequence  # type: ignore
from PyQt5.QtWidgets import (  # type: ignore
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QShortcut,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from config import APP_NAME, SUPPORT_EMAIL
from core.optimizer import (
    liberar_ram,
    limpar_cache,
    modo_gamer,
    modo_turbo,
    modo_ultra_mega,
    otimizar_processos,
)
from services.ai import responder
from services.api_client import ApiClient, ApiClientError
from services.dev_console import (
    build_alvo,
    build_os_atual,
    checklist_publicacao,
    criar_projeto,
    gerar_pacote_universal,
    listar_historico,
    registrar_historico,
)


class MainWindow(QWidget):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.user = session["user"]
        self.client = ApiClient()
        self.ai_mode = "normal"

        self.dev_process = QProcess(self)
        self.dev_process.readyReadStandardOutput.connect(self._on_process_stdout)
        self.dev_process.readyReadStandardError.connect(self._on_process_stderr)
        self.dev_process.finished.connect(self._on_process_finished)

        self.setWindowTitle(f"{APP_NAME} // Painel Inteligente")
        self.resize(1240, 980)

        layout = QVBoxLayout()

        self.label = QLabel(f"Painel {APP_NAME} - IA de Otimizacao")
        self.label.setStyleSheet("font-size: 24px; font-weight: 700;")

        self.user_label = QLabel(
            f"Usuario: {self.user['name']} | Email: {self.user['email']}"
        )
        self.plan_label = QLabel(
            f"Plano: {self.user['plan']} | Perfil: {self.user['role']} | "
            f"Licenca: {self.user['license_key']}"
        )
        self.support_label = QLabel(f"Suporte: {SUPPORT_EMAIL}")

        botoes_layout = QGridLayout()

        self.botao1 = QPushButton("Limpar Cache")
        self.botao2 = QPushButton("Liberar RAM")
        self.botao3 = QPushButton("Otimizar Processos")
        self.botao4 = QPushButton("Modo Turbo")
        self.botao5 = QPushButton("Modo Ultra Mega")
        self.botao6 = QPushButton("Modo Gamer")

        self.botao1.clicked.connect(self.cache)
        self.botao2.clicked.connect(self.ram)
        self.botao3.clicked.connect(self.processos)
        self.botao4.clicked.connect(self.turbo)
        self.botao5.clicked.connect(self.ultra)
        self.botao6.clicked.connect(self.gamer)

        botoes_layout.addWidget(self.botao1, 0, 0)
        botoes_layout.addWidget(self.botao2, 0, 1)
        botoes_layout.addWidget(self.botao3, 1, 0)
        botoes_layout.addWidget(self.botao4, 1, 1)
        botoes_layout.addWidget(self.botao5, 2, 0)
        botoes_layout.addWidget(self.botao6, 2, 1)

        self.input_ai = QTextEdit()
        self.input_ai.setMinimumHeight(120)
        self.input_ai.setPlaceholderText(
            "Pergunte para a IA: jogo/fps, startup, RAM, cache, ultra mega, apps, API..."
        )

        self.botao_ai_mode = QPushButton("IA: Modo Normal")
        self.botao_ai_mode.clicked.connect(self.toggle_ai_mode)

        self.botao_ai = QPushButton("Perguntar IA")
        self.botao_ai.clicked.connect(self.perguntar)

        self.profile_title = QLabel("Atualizar Perfil/Admin")
        self.profile_title.setStyleSheet("font-size: 20px; font-weight: 600;")

        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Novo nome")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Novo email")
        self.senha_atual_input = QLineEdit()
        self.senha_atual_input.setPlaceholderText("Senha atual (obrigatoria)")
        self.senha_atual_input.setEchoMode(QLineEdit.Password)
        self.nova_senha_input = QLineEdit()
        self.nova_senha_input.setPlaceholderText("Nova senha (opcional)")
        self.nova_senha_input.setEchoMode(QLineEdit.Password)

        self.botao_atualizar = QPushButton("Salvar Perfil")
        self.botao_atualizar.clicked.connect(self.atualizar_perfil)

        self.dev_tabs = QTabWidget()
        self.dev_tabs.setMinimumHeight(360)
        self._build_dev_tabs()
        self._setup_shortcuts()

        self.resposta = QLabel("")
        self.resposta.setWordWrap(True)
        self.resposta.setStyleSheet("font-size: 14px;")

        layout.addWidget(self.label)
        layout.addWidget(self.user_label)
        layout.addWidget(self.plan_label)
        layout.addWidget(self.support_label)
        layout.addLayout(botoes_layout)
        layout.addWidget(self.input_ai)
        layout.addWidget(self.botao_ai_mode)
        layout.addWidget(self.botao_ai)
        layout.addWidget(self.profile_title)
        layout.addWidget(self.nome_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.senha_atual_input)
        layout.addWidget(self.nova_senha_input)
        layout.addWidget(self.botao_atualizar)
        layout.addWidget(self.dev_tabs)
        layout.addWidget(self.resposta)

        self.setLayout(layout)



    def _setup_shortcuts(self):
        self.shortcut_run = QShortcut(QKeySequence("Ctrl+Return"), self)
        self.shortcut_run.activated.connect(self.dev_terminal_run)

        self.shortcut_clear = QShortcut(QKeySequence("Ctrl+L"), self)
        self.shortcut_clear.activated.connect(self.dev_terminal_clear)

        self.shortcut_history = QShortcut(QKeySequence("Ctrl+K"), self)
        self.shortcut_history.activated.connect(self.dev_terminal_history)

    def _build_dev_tabs(self):
        # LOGS TAB
        logs_tab = QWidget()
        logs_layout = QVBoxLayout()
        self.dev_logs_output = QTextEdit()
        self.dev_logs_output.setReadOnly(True)
        self.dev_logs_output.setPlainText("[Dev Console] Logs iniciais.")
        logs_layout.addWidget(self.dev_logs_output)
        logs_tab.setLayout(logs_layout)

        # BUILD TAB
        build_tab = QWidget()
        build_layout = QVBoxLayout()
        self.botao_dev_build = QPushButton("Build SO Atual")
        self.botao_dev_build.clicked.connect(self.dev_build)
        self.botao_dev_checklist = QPushButton("Checklist Publicacao")
        self.botao_dev_checklist.clicked.connect(self.dev_checklist)
        self.botao_dev_universal = QPushButton("Gerar Pacote Universal")
        self.botao_dev_universal.clicked.connect(self.dev_pacote_universal)

        build_grid = QGridLayout()
        self.botao_build_windows = QPushButton("Build Windows")
        self.botao_build_linux = QPushButton("Build Linux")
        self.botao_build_macos = QPushButton("Build macOS")
        self.botao_build_arch = QPushButton("Build Arch")
        self.botao_build_android = QPushButton("Build Android")

        self.botao_build_windows.clicked.connect(lambda: self.dev_build_alvo("windows"))
        self.botao_build_linux.clicked.connect(lambda: self.dev_build_alvo("linux"))
        self.botao_build_macos.clicked.connect(lambda: self.dev_build_alvo("macos"))
        self.botao_build_arch.clicked.connect(lambda: self.dev_build_alvo("arch"))
        self.botao_build_android.clicked.connect(lambda: self.dev_build_alvo("android"))

        build_grid.addWidget(self.botao_build_windows, 0, 0)
        build_grid.addWidget(self.botao_build_linux, 0, 1)
        build_grid.addWidget(self.botao_build_macos, 1, 0)
        build_grid.addWidget(self.botao_build_arch, 1, 1)
        build_grid.addWidget(self.botao_build_android, 2, 0, 1, 2)

        self.dev_build_output = QTextEdit()
        self.dev_build_output.setReadOnly(True)
        self.dev_build_output.setMinimumHeight(150)

        build_layout.addWidget(self.botao_dev_build)
        build_layout.addWidget(self.botao_dev_checklist)
        build_layout.addWidget(self.botao_dev_universal)
        build_layout.addLayout(build_grid)
        build_layout.addWidget(self.dev_build_output)
        build_tab.setLayout(build_layout)

        # TERMINAL TAB
        terminal_tab = QWidget()
        terminal_layout = QVBoxLayout()
        self.dev_cmd_input = QLineEdit()
        self.dev_cmd_input.setPlaceholderText(
            "Comando dev (ex: python -m unittest discover -s tests -p '*test.py')"
        )
        self.botao_dev_run = QPushButton("Executar Comando")
        self.botao_dev_run.clicked.connect(self.dev_terminal_run)
        self.botao_dev_stop = QPushButton("Parar Comando")
        self.botao_dev_stop.clicked.connect(self.dev_terminal_stop)
        self.botao_dev_history = QPushButton("Historico de Comandos")
        self.botao_dev_history.clicked.connect(self.dev_terminal_history)
        self.dev_terminal_output = QTextEdit()
        self.dev_terminal_output.setReadOnly(True)

        terminal_layout.addWidget(self.dev_cmd_input)
        terminal_layout.addWidget(self.botao_dev_run)
        terminal_layout.addWidget(self.botao_dev_stop)
        terminal_layout.addWidget(self.botao_dev_history)
        terminal_layout.addWidget(self.dev_terminal_output)
        terminal_tab.setLayout(terminal_layout)

        # TEMPLATES TAB
        templates_tab = QWidget()
        templates_layout = QVBoxLayout()
        self.dev_nome_input = QLineEdit()
        self.dev_nome_input.setPlaceholderText("Nome do projeto (ex: meu_app)")
        self.botao_dev_criar = QPushButton("Criar Projeto")
        self.botao_dev_criar.clicked.connect(self.dev_criar_projeto)
        self.templates_output = QTextEdit()
        self.templates_output.setReadOnly(True)

        templates_layout.addWidget(self.dev_nome_input)
        templates_layout.addWidget(self.botao_dev_criar)
        templates_layout.addWidget(self.templates_output)
        templates_tab.setLayout(templates_layout)

        self.dev_tabs.addTab(logs_tab, "Logs")
        self.dev_tabs.addTab(build_tab, "Build")
        self.dev_tabs.addTab(terminal_tab, "Terminal")
        self.dev_tabs.addTab(templates_tab, "Templates")

    def _log(self, msg):
        self.dev_logs_output.append(msg)

    def cache(self):
        msg = limpar_cache()
        self.resposta.setText(msg)
        self._log(msg)

    def ram(self):
        msg = liberar_ram()
        self.resposta.setText(msg)
        self._log(msg)

    def processos(self):
        msg = otimizar_processos()
        self.resposta.setText(msg)
        self._log(msg)

    def turbo(self):
        msg = modo_turbo()
        self.resposta.setText(msg)
        self._log("Modo Turbo executado")

    def ultra(self):
        msg = modo_ultra_mega()
        self.resposta.setText(msg)
        self._log("Modo Ultra Mega executado")

    def gamer(self):
        msg = modo_gamer()
        self.resposta.setText(msg)
        self._log("Modo Gamer executado")

    def toggle_ai_mode(self):
        self.ai_mode = "developer" if self.ai_mode == "normal" else "normal"
        label = "IA: Modo Desenvolvedor" if self.ai_mode == "developer" else "IA: Modo Normal"
        self.botao_ai_mode.setText(label)
        self._log(f"IA alterada para {self.ai_mode}")

    def perguntar(self):
        pergunta = self.input_ai.toPlainText()
        msg = responder(
            pergunta,
            plano=self.user["plan"],
            role=self.user["role"],
            modo=self.ai_mode,
        )
        self.resposta.setText(msg)
        self._log("Pergunta enviada para IA")

    def atualizar_perfil(self):
        senha_atual = self.senha_atual_input.text().strip()
        if not senha_atual:
            self.resposta.setText("Informe a senha atual para atualizar o perfil.")
            return

        try:
            resposta = self.client.update_profile(
                email=self.user["email"],
                current_password=senha_atual,
                new_name=self.nome_input.text().strip() or None,
                new_email=self.email_input.text().strip() or None,
                new_password=self.nova_senha_input.text().strip() or None,
            )
        except ApiClientError as exc:
            self.resposta.setText(f"Falha ao atualizar perfil: {exc}")
            self._log("Falha ao atualizar perfil")
            return

        if resposta.get("status") != "ok":
            self.resposta.setText(resposta.get("message", "Nao foi possivel atualizar perfil."))
            return

        self.user = resposta["user"]
        self.user_label.setText(f"Usuario: {self.user['name']} | Email: {self.user['email']}")
        self.plan_label.setText(
            f"Plano: {self.user['plan']} | Perfil: {self.user['role']} | "
            f"Licenca: {self.user['license_key']}"
        )
        self.resposta.setText("Perfil atualizado com sucesso. Use o novo email no proximo login.")
        self._log("Perfil atualizado")

    def dev_criar_projeto(self):
        nome = self.dev_nome_input.text().strip()
        msg = criar_projeto(nome)
        self.templates_output.setPlainText(msg)
        self.resposta.setText(msg)
        self._log(msg)

    def dev_build(self):
        msg = build_os_atual()
        self.dev_build_output.setPlainText(msg)
        self.resposta.setText(msg)
        self._log("Build SO atual executado")

    def dev_build_alvo(self, alvo):
        msg = build_alvo(alvo)
        self.dev_build_output.setPlainText(msg)
        self.resposta.setText(msg)
        self._log(f"Build alvo executado: {alvo}")

    def dev_checklist(self):
        msg = checklist_publicacao()
        self.dev_build_output.setPlainText(msg)
        self.resposta.setText(msg)
        self._log("Checklist de publicacao exibido")

    def dev_terminal_run(self):
        comando = self.dev_cmd_input.text().strip()
        if not comando:
            self.resposta.setText("Digite um comando para executar.")
            return

        if self.dev_process.state() != QProcess.NotRunning:
            self.resposta.setText("Ja existe um comando em execucao. Pare antes de iniciar outro.")
            return

        registrar_historico(comando)
        self.dev_terminal_output.setPlainText(f"$ {comando}\n")
        self.resposta.setText("Executando comando no Terminal Dev...")
        self._log(f"Terminal run: {comando}")

        self.dev_process.setWorkingDirectory(str(Path(__file__).resolve().parent.parent))

        import platform as _p

        if _p.system() == "Windows":
            self.dev_process.start("cmd.exe", ["/c", comando])
        else:
            self.dev_process.start("bash", ["-lc", comando])

    def dev_terminal_stop(self):
        if self.dev_process.state() == QProcess.NotRunning:
            self.resposta.setText("Nenhum comando em execucao para parar.")
            return
        self.dev_process.kill()
        self.resposta.setText("Comando interrompido pelo usuario.")
        self._log("Terminal: comando interrompido")

    def dev_terminal_history(self):
        self.dev_terminal_output.setPlainText(listar_historico())
        self.resposta.setText("Historico de comandos atualizado.")
        self._log("Historico exibido")

    def _on_process_stdout(self):
        out = bytes(self.dev_process.readAllStandardOutput()).decode("utf-8", errors="ignore")
        self.dev_terminal_output.moveCursor(self.dev_terminal_output.textCursor().End)
        self.dev_terminal_output.insertPlainText(out)

    def _on_process_stderr(self):
        err = bytes(self.dev_process.readAllStandardError()).decode("utf-8", errors="ignore")
        self.dev_terminal_output.moveCursor(self.dev_terminal_output.textCursor().End)
        self.dev_terminal_output.insertPlainText(err)

    def _on_process_finished(self, code, _status):
        self.resposta.setText(f"Terminal Dev finalizado com codigo {code}.")
        self._log(f"Terminal finalizado (exit={code})")


    def dev_pacote_universal(self):
        msg = gerar_pacote_universal()
        self.dev_build_output.setPlainText(msg)
        self.resposta.setText(msg)
        self._log("Pacote universal gerado")

    def dev_terminal_clear(self):
        self.dev_terminal_output.clear()
        self.resposta.setText("Terminal limpo.")
        self._log("Terminal limpo (Ctrl+L)")
