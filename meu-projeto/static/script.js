const gameSelect = document.getElementById('gameselect')
const questionInput = document.getElementById('questioninput')
const askbutton = document.getElementById('askbutton')
const form = document.getElementById('form')
const airesponse = document.getElementById('airesponse')
const flaskURL = "https://sitefln7.onrender.com/api/pergunta";


const markdownToHTML = (text) => {
    const converter = new showdown.Converter()
    return converter.makeHtml(text)
}




const perguntarIA = async (question, game) => {
  const response = await fetch(flaskURL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      mensagem: question,
      jogo: game
    })
  });

  const data = await response.json();
  return data.candidates?.[0]?.content?.parts?.[0]?.text || "Não houve resposta da IA";
};



const enviarformulario = async (event) => {
    event.preventDefault()
    const game = gameSelect.value
    const question = questionInput.value


    if(game == '' || question == '') {
        alert('Please, fill out all fields')
        return

    }

    askbutton.disabled = true
    askbutton.textContent = 'asking...'
    askbutton.classList.add('loading')
    

    //Caso dê erro no gemini
    try {
        //Perguntar para IA
        const text = await perguntarIA(question, game)
        airesponse.querySelector('.response_content').innerHTML = markdownToHTML(text)
        airesponse.classList.remove('hidden')



    } catch(error) {
        console.log('Error: ', error)
    } finally {
        askbutton.disabled = false
        askbutton.textContent = 'To Ask'
        askbutton.classList.remove('loading')
        questionInput == ''
    }
    
}

form.addEventListener('submit', enviarformulario)










