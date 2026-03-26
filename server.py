from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "AUREXA API ONLINE 🚀"

licencas = {
    "CLIENTE-001": True,
    "AUREXA-OWNER-777": True
}

@app.route("/verificar", methods=["POST"])
def verificar():
    data = request.get_json(silent=True) or {}
    chave = data.get("chave")

    if chave in licencas:
        return jsonify({"status": "ok"})
    else:
        return jsonify({"status": "erro"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
