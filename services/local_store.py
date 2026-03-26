import json
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone

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
            "price_brl": 39.90,
            "features": [
                "Otimizacao completa",
                "IA com respostas aprimoradas",
                "Suporte prioritario",
                "Publicacao de apps com marca KVP",
            ],
        },
        {
            "id": "pro",
            "name": "Pro",
            "price_brl": 99.90,
            "features": [
                "Todos os recursos Premium",
                "Multi dispositivo",
                "Relatorios e gestao avancada",
                "Workspace para criar e vender apps",
            ],
        },
    ],
    "users": [
        {
            "name": "Karollyne Pinheiro",
            "email": OWNER_EMAIL,
            "password": OWNER_PASSWORD,
            "role": "owner",
            "plan": "pro",
            "license_key": "KVP-OWNER-777",
            "status": "active",
            "devices": [],
        },
        {
            "name": "Cliente Free",
            "email": "free@fenix-boreal.com.br",
            "password": "free123",
            "role": "user",
            "plan": "free",
            "license_key": "KVP-FREE-001",
            "status": "active",
            "devices": [],
        },
        {
            "name": "Cliente Premium",
            "email": "premium@fenix-boreal.com.br",
            "password": "premium123",
            "role": "user",
            "plan": "premium",
            "license_key": "KVP-PREMIUM-001",
            "status": "active",
            "devices": [],
        },
        {
            "name": "Cliente Pro",
            "email": "pro@fenix-boreal.com.br",
            "password": "pro123",
            "role": "user",
            "plan": "pro",
            "license_key": "KVP-PRO-001",
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



def update_user_profile(email, current_password, new_name=None, new_email=None, new_password=None):
    db = load_db()
    email_normalizado = email.strip().lower()

    target_user = None
    for user in db["users"]:
        if user["email"].lower() == email_normalizado:
            target_user = user
            break

    if not target_user:
        return {"status": "error", "message": "Usuario nao encontrado."}

    if target_user["password"] != current_password:
        return {"status": "error", "message": "Senha atual invalida."}

    if new_email:
        novo_email = new_email.strip().lower()
        for user in db["users"]:
            if user is not target_user and user["email"].lower() == novo_email:
                return {"status": "error", "message": "Email ja esta em uso."}
        target_user["email"] = novo_email

    if new_name:
        target_user["name"] = new_name.strip()

    if new_password:
        target_user["password"] = new_password

    save_db(db)

    return {
        "status": "ok",
        "message": "Perfil atualizado com sucesso.",
        "user": {
            "name": target_user["name"],
            "email": target_user["email"],
            "role": target_user["role"],
            "plan": target_user["plan"],
            "license_key": target_user["license_key"],
            "status": target_user["status"],
            "devices": target_user["devices"],
        },
    }



def get_stats():
    db = load_db()
    users = db.get("users", [])
    plans = db.get("plans", [])

    return {
        "users_total": len(users),
        "users_active": len([u for u in users if u.get("status") == "active"]),
        "owners_total": len([u for u in users if u.get("role") == "owner"]),
        "plans_total": len(plans),
        "devices_total": sum(len(u.get("devices", [])) for u in users),
    }



def get_dashboard_data():
    db = load_db()
    users = db.get("users", [])

    users_view = []
    recent_devices = []
    for user in users:
        devices = user.get("devices", [])
        for index, device in enumerate(reversed(devices)):
            recent_devices.append(
                {
                    "user_name": user.get("name"),
                    "user_email": user.get("email"),
                    "device_name": device.get("device_name", "dispositivo-desconhecido"),
                    "platform": device.get("platform", "unknown"),
                    "order": index,
                }
            )
        users_view.append(
            {
                "name": user.get("name"),
                "email": user.get("email"),
                "role": user.get("role"),
                "plan": user.get("plan"),
                "status": user.get("status"),
                "devices_count": len(devices),
            }
        )

    online_users = [u for u in users_view if u.get("status") == "active"]
    devices_total = sum(u["devices_count"] for u in users_view)
    plans_counter = Counter(user.get("plan", "unknown") for user in users_view)
    platforms_counter = Counter()
    for user in users:
        for device in user.get("devices", []):
            platform = (device.get("platform") or "unknown").strip().lower()
            platforms_counter[platform] += 1

    total_users = len(users_view)
    total_online = len(online_users)
    online_rate = round((total_online / total_users) * 100, 1) if total_users else 0

    alerts = []
    if total_users and total_online == total_users:
        alerts.append(
            {
                "level": "positive",
                "title": "Base totalmente ativa",
                "message": "Todos os usuarios cadastrados estao com status ativo neste momento.",
            }
        )
    if devices_total == 0:
        alerts.append(
            {
                "level": "warning",
                "title": "Nenhum dispositivo registrado",
                "message": "Ainda nao existem dispositivos conectados na base local.",
            }
        )
    if plans_counter.get("free", 0) >= max(plans_counter.get("premium", 0), plans_counter.get("pro", 0)):
        alerts.append(
            {
                "level": "info",
                "title": "Espaco para upgrade comercial",
                "message": "A maior parte da base ainda esta em Free. Vale destacar beneficios Premium e Pro.",
            }
        )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "users_total": total_users,
        "users_online": total_online,
        "devices_total": devices_total,
        "online_rate": online_rate,
        "online_users": online_users,
        "users": users_view,
        "recent_devices": recent_devices[:6],
        "plan_breakdown": [
            {"label": "Free", "value": plans_counter.get("free", 0)},
            {"label": "Premium", "value": plans_counter.get("premium", 0)},
            {"label": "Pro", "value": plans_counter.get("pro", 0)},
        ],
        "platform_breakdown": [
            {"label": "Windows", "value": platforms_counter.get("windows", 0)},
            {"label": "Linux", "value": platforms_counter.get("linux", 0)},
            {"label": "macOS", "value": platforms_counter.get("macos", 0)},
            {"label": "Android", "value": platforms_counter.get("android", 0)},
            {
                "label": "Outros",
                "value": sum(
                    value
                    for key, value in platforms_counter.items()
                    if key not in {"windows", "linux", "macos", "android"}
                ),
            },
        ],
        "alerts": alerts,
    }
