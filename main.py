from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    return "Assistant Flask no ar!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    pergunta = data.get("pergunta")
    resposta = f"Simulação de resposta para: {pergunta}"
    return jsonify({"resposta": resposta})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)