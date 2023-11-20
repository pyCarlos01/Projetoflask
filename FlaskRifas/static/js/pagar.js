function CopiaCola(qrcode){
//  Mover text para área de transferência 
    navigator.clipboard.writeText(qrcode)

//  Exibir mensagem
    mostrar()
}
    
function mostrar(){
//  Pegar notificação
    let notificacao = document.getElementById('notificacao');

//  Mostrar elemento
    notificacao.style.display='block'

//  Chamar a função para ocultar
    setTimeout(ocultar, 2000);
}

function ocultar(){
//  Pegar notificação
    let notificacao = document.getElementById('notificacao');

//  Ocultar elemento
    notificacao.style.display='none'
}


// Redirecionar o usuario
function redirect(){
    pg.forEach(i =>{
        // window.location.reload()
        console.log(i)
        if(i.status == 'Pagamento concluído'){
            window.location.href = "/loja";
        }
    setTimeout(redirect, 2000)
    });
}

setTimeout(redirect, 2000)