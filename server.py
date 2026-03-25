from flask import Flask, request, jsonify

app = Flask(__name__)

licencas = {
    "CLIENTE-001": True,
    "AUREXA-OWNER-777": True
}

@app.route("/verificar", methods=["POST"])
def verificar():
    data = request.json
    chave = data.get("chave")

    if chave in licencas:
        return jsonify({"status": "ok"})
    else:
        return jsonify({"status": "erro"})

app.run(host="0.0.0.0", port=5000)