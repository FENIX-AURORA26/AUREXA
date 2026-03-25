from flask import Flask, request, jsonify # type: ignore

app = Flask(__name__)

# banco simples (depois pode virar banco real)
licencas = {
    "AUREXA-PRO-9999": True,
    "AUREXA-TESTE": True
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