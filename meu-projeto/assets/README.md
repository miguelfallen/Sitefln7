meu python
from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from flask_cors import CORS


Flask cria o app web |
request acessa os dados que chegam via POST |
jsonfy converte respostas para JSON pro navegador entender 
Import os : importa sistema operacional uasada para acessar variaveis | 
requests : bibliotecas pra fazer requisições HTTP comunicação com API gemini
from dotenv import load_dotenv : importa a função carrega variaveis do arquivo .env


app = Flask(__name__) # Cria uma instancia do app flask, rodar como servidor web
CORS(app)
load_dotenv() #carrega o .env

API_KEY = os.getenv("GEMINI_API_KEY") #pega variavel do .env

@app.route("/api/pergunta", methods=["POST"]) #Cria uma rota HTTP chamada /api/pergunta, aceita só requisições do tipo POST
def pergunta(): # define função quando alguem acessar /api/pergunta
    dados = request.get_json() #pega dados que vieram na requisição em JSON, ex pergunta do usuario
    texto_usuario = dados.get("mensagem") #extrai o conteudo da chave que contem o texto do usuario pra IA 
    jogo = dados.get('jogo', 'League of Legends')

    prompt_base = f"""
    ## Specialty
    You are a meta assistant specialist for games. {jogo}

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
    Here is the user's question: {texto_usuario}
    """
    # Substitua o endpoint e payload conforme a Gemini espera
    resposta = requests.post( #define que estamos enviando os dados em formato JSON 
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",  # Exemplo de endpoint
        headers={"Content-Type": "application/json"},
        params={"key": API_KEY}, #adivciona a API key como parametro da URL
        json={
            "contents": [
                {"parts": [{"text": prompt_base}]} #monta o corpo de requisição com a pergunta do usuario, no fomato que o gemini espera
            ]
        }
    ) #fechamento de requisição

    if resposta.status_code == 200:
        print(resposta.text)
        return jsonify(resposta.json()) # se a requisição der certo (200 ok) retornar da IA para o navegador
    else:
        return jsonify({"erro": "Falha ao se comunicar com a IA", "detalhes": resposta.text}), 500 # se der errado ele cita esse erro

if __name__ == "__main__":
    app.run(debug=True) #inicia o servidor flask local no modo debug



flask run --host=0.0.0.0
reiniciar o servidor