import requests

url = "https://sitefln7-2.onrender.com/api/pergunta"

payload = {
    "mensagem": "Qual é o melhor campeão para subir de elo?",
    "jogo": "League of Legends"
}

headers = {
    "Content-Type": "application/json"
}

try:
    resposta = requests.post(url, json=payload, headers=headers, timeout=20)

    if resposta.status_code == 200:
        conteudo = resposta.json()
        print("✅ Resposta da IA:")
        print(conteudo)
    else:
        print("⚠️ Erro ao chamar a API:")
        print(resposta.status_code)
        print(resposta.text)

except Exception as e:
    print("💥 Erro inesperado:")
    print(str(e))