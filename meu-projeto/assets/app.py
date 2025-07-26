from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

@app.route("/api/pergunta", methods=["POST"])
def pergunta():
    dados = request.get_json()
    texto_usuario = dados.get("mensagem")
    jogo = dados.get("jogo", "League of Legends")

    prompt_base = f""" You are a meta assistant specialist for games. {jogo}

## Task
You must answer the user's questions based on your knowledge of the game, strategies, builds, and tips.

## Rules
- If you don't know the answer, reply with 'I Don't Know' and don't try to make up an answer.
- If the question is not related to the game, respond with 'This question is not related to the game.'
- Consider the current date {datetime.now().strftime('%d/%m/%Y')}
- Conduct updated research on the current patch, based on the current date, to provide a coherent response.
= Never answer items that you are not sure exist in the current patch.

## Answer
- Save on the response, be direct and respond with a maximum of 800 characters.
- Answer in MarkDown
- There is no need to make any greetings or farewells, just respond to what the user is wanting.

## Example of response
- User question: Best Rengar jungle build
- Answer: The latest build is:

**Items:**

Put the items here.

Example of runes

___
Here is the user's question: {texto_usuario}"""  # ← Aqui entra o prompt inteiro que você criou

    resposta = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
        headers={"Content-Type": "application/json"},
        params={"key": API_KEY},
        json={
            "contents": [
                {"parts": [{"text": prompt_base}]}
            ]
        }
    )

    if resposta.status_code == 200:
        print(resposta.text)
        return jsonify(resposta.json())
    else:
        return jsonify({"erro": "Falha ao se comunicar com a IA", "detalhes": resposta.text}), 500

if __name__ == "__main__":
    app.run(debug=True)