import socket

from flask import Flask, jsonify, request, send_from_directory

from config import APP_NAME
from services.local_store import (
    get_dashboard_data,
    get_plans,
    get_stats,
    get_user_by_email,
    register_device,
    update_user_profile,
    verify_user,
)

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response


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


def _local_ip_candidates():
    hosts = {"127.0.0.1", "localhost"}
    try:
        hostname = socket.gethostname()
        hosts.add(socket.gethostbyname(hostname))
    except Exception:
        pass
    return sorted(hosts)


@app.route("/")
def home():
    return jsonify(
        {
            "app": APP_NAME,
            "status": "online",
            "message": f"{APP_NAME} API ONLINE",
            "version": "2.0",
            "features": [
                "auth.login",
                "licenses.verify",
                "users.update",
                "plans.list",
                "landing.page",
                "server.stats",
            ],
            "quick_links": {
                "health": "/health",
                "landing": "/landing",
                "plans": "/plans",
                "stats": "/server/stats",
                "dashboard": "/dashboard",
                "device_connect": "/server/device-connect-info",
            },
        }
    )


@app.route("/server/ping")
def ping():
    return jsonify({"status": "ok", "app": APP_NAME, "message": "pong"})


@app.route("/server/stats")
def stats():
    return jsonify({"status": "ok", "app": APP_NAME, "stats": get_stats()})


@app.route("/server/device-connect-info")
def device_connect_info():
    hosts = _local_ip_candidates()
    urls = [f"http://{host}:5000" for host in hosts]
    return jsonify(
        {
            "status": "ok",
            "app": APP_NAME,
            "hint": "Use uma URL da mesma rede Wi-Fi no seu celular/dispositivo.",
            "urls": urls,
        }
    )




@app.route("/server/dashboard-data")
def dashboard_data():
    return jsonify({"status": "ok", "app": APP_NAME, "data": get_dashboard_data()})


@app.route("/dashboard")
def dashboard_page():
    return send_from_directory("web", "dashboard.html")


@app.route("/dashboard/assets/<path:filename>")
def dashboard_assets(filename):
    return send_from_directory("web/assets", filename)

@app.route("/landing")
def landing_page():
    return send_from_directory("web", "index.html")


@app.route("/landing/assets/<path:filename>")
def landing_assets(filename):
    return send_from_directory("web/assets", filename)


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

    if device_name or platform_name:
        devices = register_device(email, device_name, platform_name)
    else:
        devices = user.get("devices", [])

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


@app.route("/users/update", methods=["POST"])
def update_user():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip()
    current_password = data.get("current_password") or ""

    result = update_user_profile(
        email=email,
        current_password=current_password,
        new_name=data.get("new_name"),
        new_email=data.get("new_email"),
        new_password=data.get("new_password"),
    )

    status_code = 200 if result.get("status") == "ok" else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
