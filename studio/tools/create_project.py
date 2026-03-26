from pathlib import Path

TEMPLATE = '''# {name}\n\nProjeto criado pelo KVP_STUDIO Dev Area.\n\n## Rodar\n\n```bash\npython main.py\n```\n'''
MAIN = '''def main():\n    print("{name} iniciado com KVP_STUDIO")\n\n\nif __name__ == "__main__":\n    main()\n'''


def create_project(name):
    root = Path(__file__).resolve().parent.parent
    target = root / name
    target.mkdir(parents=True, exist_ok=True)

    (target / "README.md").write_text(TEMPLATE.format(name=name), encoding="utf-8")
    (target / "main.py").write_text(MAIN.format(name=name), encoding="utf-8")

    print(f"Projeto criado em: {target}")


if __name__ == "__main__":
    project_name = input("Nome do novo projeto: ").strip() or "novo_app"
    create_project(project_name)
