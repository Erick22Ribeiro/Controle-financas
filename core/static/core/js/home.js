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

function fecharModalConta() {
    document.querySelector('.caixa-excluir-conta').style.display = 'none';
}

/* Btn info */
function exibirInfoTran(e) {
    e.stopPropagation(); // impede fechar ao abrir
    document.querySelector('.caixa-info-tran').style.display = 'block';
}
function exibirInfoCate(e) {
    e.stopPropagation(); // impede fechar ao abrir
    document.querySelector('.caixa-info-cate').style.display = 'block';
}
function exibirInfoCont(e) {
    e.stopPropagation(); // impede fechar ao abrir
    document.querySelector('.caixa-info-cont').style.display = 'block';
}

document.addEventListener('click', function (e) {
    const caixaTran = document.querySelector('.caixa-info-tran');
    const caixaCate = document.querySelector('.caixa-info-cate');
    const caixaCont = document.querySelector('.caixa-info-cont');

    // se a caixa estiver aberta e o clique for fora dela
    if (caixaTran.style.display === 'block' && !caixaTran.contains(e.target)) {
        caixaTran.style.display = 'none';
    }

    if (caixaCate.style.display === 'block' && !caixaCate.contains(e.target)) {
        caixaCate.style.display = 'none';
    }
    if (caixaCont.style.display === 'block' && !caixaCont.contains(e.target)) {
        caixaCont.style.display = 'none';
    }
});
