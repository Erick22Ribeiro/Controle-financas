// ========================================
// TOGGLE DE RECEITA/DESPESA
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    
    // Seleciona todos os botões de toggle
    const toggleButtons = document.querySelectorAll('.toggle-btn');
    const tipoInput = document.getElementById('tipo_categoria');
    
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove a classe 'active' de todos os botões
            toggleButtons.forEach(btn => btn.classList.remove('active'));
            
            // Adiciona a classe 'active' no botão clicado
            this.classList.add('active');
            
            // Atualiza o valor do input hidden com o tipo selecionado
            const tipo = this.getAttribute('data-type');
            tipoInput.value = tipo;
            
            console.log('Tipo selecionado:', tipo); // Para debug
        });
    });
    
});


// ========================================
// TOGGLE DE FILTROS (Página de Transações)
// ========================================

function toggleFilters() {
    const filtersArea = document.getElementById('filtersArea');
    filtersArea.classList.toggle('active');
}