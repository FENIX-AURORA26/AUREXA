from flask import Flask, jsonify, request

from config import APP_NAME
from services.local_store import get_plans, get_user_by_email, register_device, verify_user

app = Flask(__name__)


def _permissions_for(role, plan):
    permissions = ["diagnostics.basic"]

    if plan in {"premium", "pro"}:
        permissions.append("assistant.enhanced")
    if plan == "pro":
        permissions.append("devices.multi")
    if role == "owner":
        permissions.extend(
            [
                "admin.full_access",
                "billing.manage",
                "licenses.manage",
                "users.manage",
            ]
        )

    return permissions


@app.route("/")
def home():
    return jsonify(
        {
            "app": APP_NAME,
            "status": "online",
            "message": "AUREXA_BOREAL API ONLINE",
        }
    )


@app.route("/health")
def health():
    return jsonify({"status": "ok", "app": APP_NAME})


@app.route("/plans")
def plans():
    return jsonify({"plans": get_plans()})


@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""
    device_name = data.get("device_name") or ""
    platform_name = data.get("platform") or ""

    user = verify_user(email, password)
    if not user:
        return jsonify({"status": "error", "message": "Email ou senha invalidos."}), 401

    devices = register_device(email, device_name, platform_name)
    permissions = _permissions_for(user["role"], user["plan"])

    return jsonify(
        {
            "status": "ok",
            "message": "Login realizado com sucesso.",
            "session": {
                "app_name": APP_NAME,
                "user": {
                    "name": user["name"],
                    "email": user["email"],
                    "role": user["role"],
                    "plan": user["plan"],
                    "license_key": user["license_key"],
                    "status": user["status"],
                    "devices": devices,
                },
                "permissions": permissions,
            },
        }
    )


@app.route("/licenses/verify", methods=["POST"])
def verify_license():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip()
    license_key = (data.get("license_key") or "").strip()
    user = get_user_by_email(email)

    if user and user["license_key"] == license_key:
        return jsonify({"status": "ok", "plan": user["plan"], "role": user["role"]})

    return jsonify({"status": "error", "message": "Licenca invalida."}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
