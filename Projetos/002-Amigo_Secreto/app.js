// Array para armazenar os nomes
let nomes = [];

// Função para adicionar um amigo à lista
function adicionarAmigo() {
    const inputNome = document.getElementById('amigo');
    const nome = inputNome.value.trim();
    const listaAmigos = document.getElementById('listaAmigos');

    if (nome === '') {
        alert('Por favor, insira um nome válido.');
        return;
    }

    nomes.push(nome);
    atualizarListaAmigos();
    inputNome.value = ''; // Limpa o campo de entrada
}

// Adiciona evento para permitir adicionar nome ao pressionar Enter
document.getElementById('amigo').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        adicionarAmigo();
    }
});

// Função para atualizar a lista exibida na tela
function atualizarListaAmigos() {
    const listaAmigos = document.getElementById('listaAmigos');
    listaAmigos.innerHTML = '';
    
    nomes.forEach(nome => {
        const li = document.createElement('li');
        li.textContent = nome;
        listaAmigos.appendChild(li);
    });
}

// Função para sortear um amigo secreto
function sortearAmigo() {
    if (nomes.length === 0) {
        alert('Adicione pelo menos um nome para realizar o sorteio.');
        return;
    }
    
    const indiceSorteado = Math.floor(Math.random() * nomes.length);
    const amigoSorteado = nomes[indiceSorteado];
    
    const resultado = document.getElementById('resultado');
    resultado.innerHTML = `<li>Amigo secreto sorteado: <strong>${amigoSorteado}</strong></li>`;
}
