from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("Osk-proj-8Ay8NPOeVsIuG2M9CJbgU-w7nY3wU2BZxqsUXmoAvDlxEcRwk_1hwxn5ird_VXGt4JYMScpsw7T3BlbkFJDf1F5scnJp0w43tP2a04Rz4bWxwsLvPbUEWGcbMUwKQpE4cyqhE_eRrs3BKm-_vAQMTXou93QA"))

ASSISTANT_ID = "asst_4LQKOMcVXh4ZNUsDAAXGG4Ge"

@app.route("/query", methods=["POST"])
def buscar_normativo():
    data = request.get_json()
    pergunta = data.get("pergunta")

    if not pergunta:
        return jsonify({"erro": "Campo 'pergunta' é obrigatório"}), 400

    try:
        # Cria um novo thread para a conversa
        thread = client.beta.threads.create()

        # Adiciona a mensagem do usuário ao thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=pergunta
        )

        # Executa o assistant com a vector store conectada
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID,
        )

        # Aguarda até a execução finalizar
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == "completed":
                break

        # Obtém a resposta final
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        resposta = messages.data[0].content[0].text.value

        return jsonify({"resposta": resposta})

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)