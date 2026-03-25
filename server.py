from flask import Flask, request, jsonify 

app = Flask(__name__)

# Banco simples (depois vira banco real)
licencas = {
    "AUREXA-1234": True,
    "AUREXA-PRO-9999": True
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