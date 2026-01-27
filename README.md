# Sistema de Controle Financeiro com Análise de Dados

Este projeto consiste em um **sistema web de controle financeiro** desenvolvido com **Python e Django**, com foco na **modelagem, persistência, manipulação e análise de dados**.

Além das operações de CRUD, o sistema possui uma **camada analítica**, onde os dados financeiros são processados com **Pandas** e visualizados por meio de **gráficos interativos com Plotly**.

---

## Funcionalidades

### Gerenciamento de Dados (CRUD)
- Cadastro, edição e exclusão de:
  - Transações
  - Categorias (Receita / Despesa)
  - Contas
- Interface web integrada ao backend Django

### Modelagem de Dados
- Entidades normalizadas:
  - `Transacao`
  - `Categoria`
  - `Conta`
- Relacionamentos com `ForeignKey` via Django ORM
- Uso de `DecimalField` para valores monetários
- Organização temporal das transações

### Análise de Dados
- Extração de dados do banco via ORM
- Conversão dos dados em **DataFrames com Pandas**
- Processamento com:
  - Filtros temporais
  - Agregações mensais
  - Cálculo de receitas e despesas

### Visualização
- Gráficos interativos com **Plotly**, incluindo:
  - Comparativo de receitas e despesas
  - Distribuição de valores por categoria
  - Evolução temporal das transações

---

## 🛠️ Tecnologias Utilizadas

- Python
- Django
- Pandas
- Plotly
- HTML
- CSS
- JavaScript
- SQLite (ambiente de desenvolvimento)

---

## ⚙️ Como executar o projeto localmente

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/Erick22Ribeiro/Controle-financas.git
cd Controle-financas
