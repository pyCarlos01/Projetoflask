function cotas(id){
  
//  Limpar as Ul
    const li = document.getElementById('ulcotas');
    li.innerHTML = '';

//  Adicionar valor ao titulo do Modal, para o mesmo passar como "id" para a função campoPesquisa
    let title = document.getElementById('exampleModalLabel').title=id

//  Percorrer a constante
    rifas.forEach(i=>{
//      Verificar id do botão que está sendo clicado        
        if(parseInt(i.id_rifa) == parseInt(id)){
            let li = document.createElement('li');
            let label = document.createElement('label')
            label.innerText = i.cota
            li.style.display='inline';

            li.appendChild(label);
            let ul = document.getElementById('ulcotas');
            ul.appendChild(li);
        };
    })
}

function pesquisarCota(){
//  Pegar elementos
    let pesquisa = document.getElementById('pesquisa').value;
    
    const cotas = document.getElementsByTagName('label');
    const numeros = [];

//  Adicionar cotas percorridas em uma lista

    for(let i=0; i < cotas.length; i++){
        numeros.push(parseInt(cotas[i].innerHTML))
    }
    
//  Limpar a lista antes de pesquisar
    const li = document.getElementById('ulcotas');
    li.innerHTML = '';

//  Verificar o valor de pesquisa antes de prosseguir
    for(let i=0; i < numeros.length; i++){
//      Verificar se o valor de "pesquisa" é igual ao "número"
        if(parseInt(pesquisa) == parseInt(numeros[i])){
            let li = document.createElement('li');
            let label = document.createElement('label')
            label.innerText = numeros[i]
            li.style.display='inline';

            li.appendChild(label);
            let ul = document.getElementById('ulcotas');
            ul.appendChild(li);
        }
    }
//  Verificar se a lista de números é "vazia", caso sim retornar a mensagem "Não encontrado"
    if(li.innerHTML == ''){
//      Configuração do Label
        let li = document.createElement('li');
        let label = document.createElement('label');
        label.style.color = 'red';
        label.style.backgroundColor = 'white';
        label.innerText = 'Pesquisa sem Resultados!';

        li.style.display='inline';

        li.appendChild(label);
        let ul = document.getElementById('ulcotas');
        ul.appendChild(li);

//      Chamar a função para colocar todos os números de volta
        document.getElementById('pesquisa').value = '';

        setTimeout(campoPesquisa, 5000)
    }
}

function campoPesquisa(){
//  Pegar elementos
    let pesquisa = document.getElementById('pesquisa').value;
    let id = document.getElementById('exampleModalLabel').title;

// Caso o valor da pequisa seja igual "vazio", retornar todos os números de volta
    if(pesquisa == ''){
//      Chamar a função cotas para restaurar os números
        cotas(parseInt(id))
    }
    else{
        cotas(parseInt(id))
    }
}

function cotasCompradas(id_usuario){
//  Pegar elemento
    let p = document.getElementsByTagName('p');

//  Percorrer id
    for(let i=0; i < p.length; i++){
        buscarCota(id_usuario, p[i].id)
    }
}

function buscarCota(id_usuario, id_rifa){
// Criar lista
    const cotas = []

// Percorrer Rifas
    rifas.forEach(i=>{
        if(id_usuario == i.id_usuario && id_rifa == i.id_rifa){
            cotas.push(i.cota)
        }
    })
    // Registrar quantidades cotas
    document.getElementById(id_rifa).innerText = 'Cotas Compradas: ' + cotas.length
}