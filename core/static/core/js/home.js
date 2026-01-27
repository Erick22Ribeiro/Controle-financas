/* =============================
GERAL
============================= */
function estaVisivel(elemento) {
    return elemento && window.getComputedStyle(elemento).display !== 'none';
}

/* =============================
CATEGORIAS
============================= */

function abrirModalOpcs() {

    const caixaEditar = document.querySelector('.caixa-editar');
    const caixaExcluir = document.querySelector('.caixa-excluir');
    const caixaOpcoes = document.querySelector('.caixa-opcoes');

    // Se editar ou excluir estiverem abertas, não faz nada
    if (estaVisivel(caixaEditar) || estaVisivel(caixaExcluir)) {
        return;
    }

    else{
        caixaOpcoes.style.display = 'block';
    }


    document.querySelector('.caixa-opcoes').style.display = 'block';
}

function fecharOpcs(){
    document.querySelector('.caixa-opcoes').style.display = 'none';
}

function abrirModalExcluir() {
    document.querySelector('.caixa-opcoes').style.display = 'none';
    document.querySelector('.caixa-excluir').style.display = 'block';

}
function fecharExcluir(){
    document.querySelector('.caixa-excluir').style.display = 'none';
    document.querySelector('.caixa-opcoes').style.display = 'block';
}

function abrirModalEditar() {
    document.querySelector('.caixa-opcoes').style.display = 'none';
    document.querySelector('.caixa-editar').style.display = 'block';
}

function fecharEdit(){
    document.querySelector('.caixa-editar').style.display = 'none';
    document.querySelector('.caixa-opcoes').style.display = 'block';
}

/* EDITOR */
function editarCategoria(id) {
    const container = document.getElementById(`cat-${id}`);

    container.querySelector('.view-mode').style.display = 'none';
    container.querySelector('.edit-mode').style.display = 'flex';
}

function cancelarEdicao(id) {
    const container = document.getElementById(`cat-${id}`);

    container.querySelector('.edit-mode').style.display = 'none';
    container.querySelector('.view-mode').style.display = 'flex';
}

/* =============================
CONTAS
============================= */

function abrirModalOpcsConta(){

    const caixaEditar = document.querySelector('.caixa-editar-conta');
    const caixaExcluir = document.querySelector('.caixa-excluir-conta');
    const caixaOpcoes = document.querySelector('.caixa-opcoes-conta');

    // Se editar ou excluir estiverem abertas, não faz nada
    if (estaVisivel(caixaEditar) || estaVisivel(caixaExcluir)) {
        return;
    }

    else{
        caixaOpcoes.style.display = 'block';
    }

}

function fecharOpcsConta(){
    document.querySelector('.caixa-opcoes-conta').style.display = 'none';
}

function abrirModalExcluirConta() {
    document.querySelector('.caixa-opcoes-conta').style.display = 'none';
    document.querySelector('.caixa-excluir-conta').style.display = 'block';

}
function fecharExcluirConta(){
    document.querySelector('.caixa-excluir-conta').style.display = 'none';
    document.querySelector('.caixa-opcoes-conta').style.display = 'block';
}

function abrirModalEditarConta() {
    document.querySelector('.caixa-opcoes-conta').style.display = 'none';
    document.querySelector('.caixa-editar-conta').style.display = 'block';
}

function fecharEditConta(){
    document.querySelector('.caixa-editar-conta').style.display = 'none';
    document.querySelector('.caixa-opcoes-conta').style.display = 'block';
}

/* EDITOR */
function editarConta(id) {
    const container = document.getElementById(`cont-${id}`);

    container.querySelector('.view-mode').style.display = 'none';
    container.querySelector('.edit-mode').style.display = 'flex';
}

function cancelarEditConta(id) {
    const container = document.getElementById(`cont-${id}`);

    container.querySelector('.edit-mode').style.display = 'none';
    container.querySelector('.view-mode').style.display = 'flex';
}

















function abrirModalConta() {
   
}

function fecharModalConta() {
    document.querySelector('.caixa-excluir-conta').style.display = 'none';
}