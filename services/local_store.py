import json
from copy import deepcopy

from config import APP_NAME, DB_PATH, OWNER_EMAIL, OWNER_PASSWORD


DEFAULT_DATA = {
    "app": {"name": APP_NAME},
    "plans": [
        {
            "id": "free",
            "name": "Free",
            "price_brl": 0,
            "features": [
                "Login no desktop",
                "Diagnostico basico",
                "Suporte comunitario",
            ],
        },
        {
            "id": "premium",
            "name": "Premium",
            "price_brl": 29.90,
            "features": [
                "Otimizacao completa",
                "IA com respostas aprimoradas",
                "Suporte prioritario",
            ],
        },
        {
            "id": "pro",
            "name": "Pro",
            "price_brl": 79.90,
            "features": [
                "Todos os recursos Premium",
                "Multi dispositivo",
                "Relatorios e gestao avancada",
            ],
        },
    ],
    "users": [
        {
            "name": "Luna Boreal",
            "email": OWNER_EMAIL,
            "password": OWNER_PASSWORD,
            "role": "owner",
            "plan": "pro",
            "license_key": "AUREXA-OWNER-777",
            "status": "active",
            "devices": [],
        },
        {
            "name": "Cliente Free",
            "email": "free@fenix-boreal.com.br",
            "password": "free123",
            "role": "user",
            "plan": "free",
            "license_key": "AUREXA-FREE-001",
            "status": "active",
            "devices": [],
        },
        {
            "name": "Cliente Premium",
            "email": "premium@fenix-boreal.com.br",
            "password": "premium123",
            "role": "user",
            "plan": "premium",
            "license_key": "AUREXA-PREMIUM-001",
            "status": "active",
            "devices": [],
        },
        {
            "name": "Cliente Pro",
            "email": "pro@fenix-boreal.com.br",
            "password": "pro123",
            "role": "user",
            "plan": "pro",
            "license_key": "AUREXA-PRO-001",
            "status": "active",
            "devices": [],
        },
    ],
}


def _ensure_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not DB_PATH.exists():
        save_db(deepcopy(DEFAULT_DATA))


def load_db():
    _ensure_db()
    with DB_PATH.open("r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def save_db(data):
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DB_PATH.open("w", encoding="utf-8") as arquivo:
        json.dump(data, arquivo, indent=2, ensure_ascii=True)


def get_user_by_email(email):
    db = load_db()
    email_normalizado = email.strip().lower()
    for user in db["users"]:
        if user["email"].lower() == email_normalizado:
            return user
    return None


def verify_user(email, password):
    user = get_user_by_email(email)
    if not user:
        return None
    if user["password"] != password:
        return None
    if user["status"] != "active":
        return None
    return user


def register_device(email, device_name, platform_name):
    db = load_db()
    email_normalizado = email.strip().lower()
    for user in db["users"]:
        if user["email"].lower() == email_normalizado:
            device = {
                "device_name": device_name or "dispositivo-desconhecido",
                "platform": platform_name or "unknown",
            }
            if device not in user["devices"]:
                user["devices"].append(device)
                save_db(db)
            return user["devices"]
    return []


def get_plans():
    return load_db()["plans"]
