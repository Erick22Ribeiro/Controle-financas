/* ========================================
   FUNÇÃO DE TROCA DE ABAS (CATEGORIAS)
   ======================================== */
function switchTab(button) {
    const tipoSelecionado = button.value; // 'receita' ou 'despesa'
    const rows = document.querySelectorAll('.categoria-item');

    // Mostrar/ocultar categorias baseado no tipo
    rows.forEach(row => {
        if (row.dataset.tipo === tipoSelecionado) {
            row.style.display = 'flex';
        } else {
            row.style.display = 'none';
        }
    });

    // Marcar aba ativa
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    button.classList.add('active');
}

// Inicializar: mostrar apenas categorias de 'receita' ao carregar
document.addEventListener('DOMContentLoaded', function() {
    const primeiraAba = document.querySelector('.tab[value="receita"]');
    if (primeiraAba) {
        switchTab(primeiraAba);
    }
});

/* ========================================
   TRANSAÇÕES - EDITAR/CANCELAR
   ======================================== */
function editarTransacao(btn) {
    const item = btn.closest('.transacao-item');
    
    // Esconder modo visualização
    item.querySelector('.view-mode').style.display = 'none';
    
    // Mostrar modo edição
    item.querySelector('.edit-mode').style.display = 'flex';
}

function cancelarTransacao(btn) {
    const item = btn.closest('.transacao-item');
    
    // Esconder modo edição
    item.querySelector('.edit-mode').style.display = 'none';
    
    // Mostrar modo visualização
    item.querySelector('.view-mode').style.display = 'flex';
    
    // Resetar valores do formulário (opcional, mas recomendado)
    const form = item.querySelector('.edit-form');
    if (form) {
        form.reset();
    }
}

/* ========================================
   CONTAS - EDITAR/CANCELAR
   ======================================== */
function editarConta(btn) {
    const item = btn.closest('.conta-item');
    
    // Esconder modo visualização
    item.querySelector('.view-mode').style.display = 'none';
    
    // Mostrar modo edição
    item.querySelector('.edit-mode').style.display = 'flex';
}

function cancelarConta(btn) {
    const item = btn.closest('.conta-item');
    
    // Esconder modo edição
    item.querySelector('.edit-mode').style.display = 'none';
    
    // Mostrar modo visualização
    item.querySelector('.view-mode').style.display = 'flex';
    
    // Resetar valores do formulário
    const form = item.querySelector('.edit-form');
    if (form) {
        form.reset();
    }
}

/* ========================================
   CATEGORIAS - EDITAR/CANCELAR
   ======================================== */
function editarCategoria(btn) {
    const item = btn.closest('.categoria-item');
    
    // Esconder modo visualização
    item.querySelector('.view-mode').style.display = 'none';
    
    // Mostrar modo edição
    item.querySelector('.edit-mode').style.display = 'flex';
}

function cancelarCategoria(btn) {
    const item = btn.closest('.categoria-item');
    
    // Esconder modo edição
    item.querySelector('.edit-mode').style.display = 'none';
    
    // Mostrar modo visualização
    item.querySelector('.view-mode').style.display = 'flex';
    
    // Resetar valores do formulário
    const form = item.querySelector('.edit-form');
    if (form) {
        form.reset();
    }
}