function abrirModalOpcs() {
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



function fecharModal() {
    document.querySelector('.caixa-excluir').style.display = 'none';
}

function abrirModalConta() {
    document.querySelector('.caixa-excluir-conta').style.display = 'block';
}

function fecharModalConta() {
    document.querySelector('.caixa-excluir-conta').style.display = 'none';
}



function editarCategoria(id) {
    const container = document.getElementById(`cat-${id}`);

    console.log('foi')

    container.querySelector('.view-mode').style.display = 'none';
    container.querySelector('.edit-mode').style.display = 'flex';
}

function cancelarEdicao(id) {
    const container = document.getElementById(`cat-${id}`);

    container.querySelector('.edit-mode').style.display = 'none';
    container.querySelector('.view-mode').style.display = 'flex';
}

