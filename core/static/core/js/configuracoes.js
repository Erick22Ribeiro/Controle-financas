function switchTab(button) {
    const tipoSelecionado = button.value; // receita ou despesa
    const rows = document.querySelectorAll('.row.cat');

    rows.forEach(row => {
        if (row.dataset.tipo === tipoSelecionado) {
            row.style.display = 'flex';
        } else {
            row.style.display = 'none';
        }
    });

    // opcional: marcar aba ativa
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    button.classList.add('active');
}
