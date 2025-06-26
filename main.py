from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Pegando as variáveis do ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_input = data.get("message", "")

    try:
        thread = openai.beta.threads.create()
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )
        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        # Espera ativa (simples) até resposta estar pronta
        while True:
            run_status = openai.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == "completed":
                break

        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        answer = messages.data[0].content[0].text.value

        return jsonify({"response": answer})

    except Exception as e:
        return jsonify({"response": f"Erro: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")