from flask import Flask, request, jsonify, render_template, send_from_directory # <<< ADICIONEI render_template e send_from_directory
from flask_cors import CORS
from datetime import datetime
import requests
import os

# <<< MODIFIQUEI ESTA LINHA para incluir static_folder e template_folder
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

API_KEY = os.getenv("GEMINI_API_KEY")

# 🏠 Rota principal para servir o frontend <<< ALTEREI ESTA ROTA
@app.route("/")
def home():
    return render_template("index.html") # <<< AGORA ELA RETORNA SEU HTML

# 🚀 Rota principal de perguntas
@app.route("/api/pergunta", methods=["POST"])
def pergunta():
    try:
        dados = request.get_json()

        if not dados or "mensagem" not in dados:
            return jsonify({"erro": "Campo 'mensagem' é obrigatório."}), 400

        texto_usuario = dados.get("mensagem")
        jogo = dados.get("jogo", "League of Legends")

        prompt = f"""
You are a meta assistant specialist for games. {jogo}

## Task
You must answer the user's questions based on your knowledge of the game, strategies, builds, and tips.

## Rules
- If you don't know the answer, reply with 'I Don't Know' and don't try to make up an answer.
- If the question is not related to the game, respond with 'This question is not related to the game.'
- Consider the current date {datetime.now().strftime('%d/%m/%Y')}
- Conduct updated research on the current patch, based on the current date, to provide a coherent response.
- Never answer items that you are not sure exist in the current patch.

## Answer
- Save on the response, be direct and respond with a maximum of 800 characters.
- Answer in MarkDown
- No greetings or farewells.

## Example of response
- User question: Best Rengar jungle build
- Answer: The latest build is:

**Items:**

Put the items here.

Example of runes

___
Here is the user's question: {texto_usuario}
        """

        resposta = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
            headers={"Content-Type": "application/json"},
            params={"key": API_KEY},
            json={
                "contents": [
                    {"parts": [{"text": prompt}]}
                ]
            },
            timeout=40  # ⏱️ Timeout aumentado para evitar erro
        )

        if resposta.status_code == 200:
            conteudo = resposta.json()
            return jsonify(conteudo)
        else:
            return jsonify({
                "erro": "Falha ao se comunicar com a IA.",
                "status": resposta.status_code,
                "detalhes": resposta.text
            }), 500

    except Exception as e:
        return jsonify({
            "erro": "Erro interno no servidor.",
            "detalhes": str(e)
        }), 500

# Para uso local (opcional), não será usado com Gunicorn no Render
if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode)