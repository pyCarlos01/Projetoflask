function qntyCotas(id, operacao){

//  Pegar Elementos
    let btn = document.getElementById(id);
    let quantidade = document.getElementById('quantidade');
    let valor = document.getElementById('valor');

//  Ocultar o erro
    let error = document.getElementById('error');
    error.style.display = 'None';

// Verificar se a quantiade é igual a 0
    if(quantidade.value == ''){
        quantidade.value = 0;
    };

//  Quantidade Antiga
    let qnty_antiga = parseInt(quantidade.value);

//  Definir Operação Matemática a ser feita
    if(operacao == 'soma'){
        let qnty_nova = parseInt(qnty_antiga) + parseInt(btn.ariaValueText);

//      Valor final
        quantidade.value = qnty_nova;
    }
    else{
        let qnty_nova = parseInt(qnty_antiga) - parseInt(btn.ariaValueText);

//      Valor final
        quantidade.value = qnty_nova;
    };

//  Não deixar o valor ser menor que 1
    if(quantidade.value < 0){
        quantidade.value = 0
    };
    max(parseInt(quantidade.value))

//  Calcular valor da compra
    resultado = valor.innerText * quantidade.value

    rotuloValor(parseFloat(resultado).toFixed(2))
}

function max(qnty_comprada){
//  Pegar Elementos
    let vendas = document.getElementById('vendas').value;
    let cotas = document.getElementById('cotas').value;
    let reservados = document.getElementById('reservados').value;

//  Subtrair para obter a quantidade que será possível vender
    total_disp = parseInt(cotas) - parseInt(vendas) - parseInt(reservados);

//  Verificar a quantidade comprada e a quantidade disponível
    if(qnty_comprada > total_disp){
        error.value = 'Quantidade indisponível para compra, tente uma quantidade menor!'
        error.style.display = 'block';
        quantidade.value = ''
        setTimeout(mostrar, 5000)
    };
}

function mostrar(){
    error.style.display='none'
}

function rotuloValor(preco){

//  Pegar Elemento
    let comprar = document.getElementById('compras');
    let valor = document.getElementById('preco');

    comprar.innerText = parseFloat(preco).toFixed(2)
    valor.value = preco

}

function finalizar(){
    valor = document.getElementById('compras').innerText;
    let quantidade = document.getElementById('quantidade').value;

    if(valor == 0.00){
        qntyCotas('mais1', 'soma')
    }
}