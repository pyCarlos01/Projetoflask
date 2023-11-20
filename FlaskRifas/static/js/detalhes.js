function buscarCota(id_rifa){
//  Pegar elemento
    let pesquisa = document.getElementById('pesquisa').value;
    let qnt = document.getElementById('qnt').innerText;

//  Percorrer banco de dados números, parâmetros "id_rifa, cota"
    numero.forEach(i => {
        if(parseInt(id_rifa) == i.id_rifa && parseInt(pesquisa) == i.cota){
            if(i.status == 'Disponível'){
                Disponibilidade(1)
            }
            else if(i.status == 'Pago' | i.status == 'Reservado'){
                Disponibilidade(2)
                buscarUsuario(i.id_pagamento, i.id_usuario, i.status)
            }
        }
        if(parseInt(qnt) < parseInt(pesquisa)){
            Disponibilidade(0)
        }
    });
};

function buscarUsuario(id_pagamento, id_usuario, pg_status){
//  Pegar Elemento
    const ul = document.getElementById('comp');

//  Criar Elementos
    let li = document.createElement('li');
    let nome = document.createElement('label');
    let email = document.createElement('label');
    let telefone = document.createElement('label');
    let status = document.createElement('label');
    let pagamento = document.createElement('label');

//  Percorrer banco de usuario
    usuario.forEach(j=>{
        if(parseInt(id_usuario) == j.id){
            nome.innerText = 'Nome: ' + j.nome;
            email.innerText = 'E-mail: ' + j.email;
            telefone.innerText = 'Telefone: ' + j.telefone;
            status.innerText = 'Status: ' + pg_status;
            pagamento.innerText = 'Pagamento: ' + id_pagamento;

//          Configurar li e adiconar
            li.style.display='flex'
            li.style.flexDirection = 'column'
            li.appendChild(nome)
            li.appendChild(email)
            li.append(telefone)
            li.append(status)
            li.append(pagamento)
            ul.appendChild(li)
        };
    });
}

function Disponibilidade(disp){
//  Pegar Elementos
    const ul = document.getElementById('comp');
    let pesquisa = document.getElementById('pesquisa');
    let label = document.createElement('label');

//  Verificar e configurar o label
    if(disp == 1){
        reiniciarUl(ul)
        ul.innerText = '';
        label.innerText = 'Cota Disponível!';
        label.style.color = 'green';
        label.style.display = 'flex';
        label.style.justifyContent = 'center';
        label.style.alignItems = 'center';
        ul.appendChild(label);
    }
    else if(disp == 0){
        reiniciarUl(ul);
        ul.innerText = '';
        label.innerText = 'Cota não existe para esta rifa!';
        label.style.color = 'red';
        label.style.display = 'flex';
        label.style.justifyContent = 'center';
        label.style.alignItems = 'center';
        ul.appendChild(label);
        pesquisa.value = ""

    }
    else{
        reiniciarUl(ul);
    }
}

function reiniciarUl(ul){
    ul.innerText = '';
}