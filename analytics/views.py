from django.shortcuts import render
from core.models import Transacao
from datetime import date
from django.db.models import Sum
from django.db.models.functions import ExtractYear


import pandas as pd #analise
import plotly.express as px #exibição
from plotly.offline import plot


# Create your views here.
def dados(request):

    # =====================================================
    # 1. BUSCA DE DADOS NO BANCO (ORM)
    # -----------------------------------------------------
    # Busca todas as transações já trazendo categoria e conta
    # select_related evita queries extras (performance)
    # =====================================================
    transacoes = Transacao.objects.select_related(
        'categoria', 'conta'
    ).values(
        'descricao', 'valor', 'data',
        'categoria__nome', 'categoria__tipo',
        'conta__nome'
    )

    # =====================================================
    # 2. CONVERSÃO PARA DATAFRAME (PANDAS)
    # -----------------------------------------------------
    # Facilita análises, agrupamentos e gráficos
    # =====================================================
    df = pd.DataFrame(list(transacoes))

    # =====================================================
    # TRATAMENTO DE DATAFRAME VAZIO
    # -----------------------------------------------------
    # Se não houver transações, cria colunas vazias
    # para evitar KeyError nos próximos passos
    # =====================================================
    if df.empty:
        df = pd.DataFrame(columns=[
            'descricao', 'valor', 'data',
            'categoria', 'tipo', 'conta'
        ])

    # Renomeia colunas para nomes mais simples
    df.rename(columns={
        'categoria__nome': 'categoria',
        'categoria__tipo': 'tipo',
        'conta__nome': 'conta'
    }, inplace=True)

    # Converte a coluna data para datetime
    df['data'] = pd.to_datetime(df['data'])

    # =====================================================
    # 3. DEFINIÇÕES FIXAS (MESES)
    # -----------------------------------------------------
    # Usado no select de meses no template
    # =====================================================
    MESES = [
        (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'),
        (4, 'Abril'), (5, 'Maio'), (6, 'Junho'),
        (7, 'Julho'), (8, 'Agosto'), (9, 'Setembro'),
        (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro'),
    ]

    hoje = date.today()

    # =====================================================
    # 4. FILTROS SELECIONADOS (MÊS E ANO)
    # -----------------------------------------------------
    # Lê os filtros da URL (?mes=1&ano=2024)
    # Se não existir, usa mês e ano atuais
    # =====================================================
    mes_selecionado = request.GET.get('mes')
    if mes_selecionado:
        mes_selecionado = int(mes_selecionado)
    else:
        mes_selecionado = hoje.month

    ano_selecionado = request.GET.get('ano')
    if ano_selecionado:
        ano_selecionado = int(ano_selecionado)
    else:
        ano_selecionado = hoje.year

    # =====================================================
    # 5. CÁLCULOS DO MÊS SELECIONADO (ORM)
    # -----------------------------------------------------
    # Receita, despesa e saldo do mês/ano selecionados
    # =====================================================
    
    receita_mes = Transacao.objects.filter(
        categoria__tipo='receita',
        data__month=mes_selecionado,
        data__year=ano_selecionado,
    ).aggregate(total=Sum('valor'))['total'] or 0

    despesa_mes = Transacao.objects.filter(
        categoria__tipo='despesa',
        data__month=mes_selecionado,
        data__year=ano_selecionado,
    ).aggregate(total=Sum('valor'))['total'] or 0

    saldo_mes = receita_mes - despesa_mes

    # =====================================================
    # 6. PREPARAÇÃO DO DATAFRAME PARA ANÁLISES MENSAIS
    # -----------------------------------------------------
    # Cria colunas auxiliares para agrupamentos
    # =====================================================
    df['ano'] = df['data'].dt.year
    df['mes_num'] = df['data'].dt.month
    df['mes_nome'] = df['data'].dt.month_name(locale='pt_BR')

    # =====================================================
    # 7. RESUMO MENSAL (RECEITA X DESPESA)
    # -----------------------------------------------------
    # Agrupa por ano, mês e tipo (receita/despesa)
    # =====================================================
    resumo_mensal = (
        df.groupby(['ano', 'mes_num', 'mes_nome', 'tipo'])['valor']
        .sum()
        .reset_index()
    )

    # =====================================================
    # 8. ANOS DISPONÍVEIS (PARA SELECT DE ANO)
    # -----------------------------------------------------
    # Mostra apenas anos que possuem transações
    # =====================================================
    anos_disponiveis = (
        Transacao.objects
        .annotate(ano=ExtractYear('data'))
        .values_list('ano', flat=True)
        .distinct()
        .order_by('-ano')
    )

    # =====================================================
    # 9. MÊS COM MAIOR RECEITA
    # =====================================================
    receitas_mensais = resumo_mensal[resumo_mensal['tipo'] == 'receita']

    if not receitas_mensais.empty:
        linha = receitas_mensais.loc[receitas_mensais['valor'].idxmax()]
        mes_maior_receita = f"{linha['mes_nome']} de {linha['ano']}"
        valor_maior_receita = linha['valor']
    else:
        mes_maior_receita = None
        valor_maior_receita = 0

    # =====================================================
    # 10. MÊS COM MAIOR DESPESA
    # =====================================================
    despesas_mensais = resumo_mensal[resumo_mensal['tipo'] == 'despesa']

    if not despesas_mensais.empty:
        linha = despesas_mensais.loc[despesas_mensais['valor'].idxmax()]
        mes_maior_despesa = f"{linha['mes_nome']} de {linha['ano']}"
        valor_maior_despesa = linha['valor']
    else:
        mes_maior_despesa = None
        valor_maior_despesa = 0

    # =====================================================
    # 11. AGRUPAMENTOS POR CATEGORIA
    # -----------------------------------------------------
    # Usado nos gráficos de pizza
    # =====================================================
    despesas = df[df['tipo'] == 'despesa']
    gastos_categoria = despesas.groupby('categoria')['valor'].sum().reset_index()

    receitas = df[df['tipo'] == 'receita']
    ganhos_categoria = receitas.groupby('categoria')['valor'].sum().reset_index()

    # =====================================================
    # 12. CRIAÇÃO DOS GRÁFICOS (PLOTLY)
    # =====================================================
    g_1 = px.bar(
        resumo_mensal,
        x='mes_nome',
        y='valor',
        color='tipo',
        title='Receitas X Despesas por mês'
    )

    g_2 = px.pie(
        gastos_categoria,
        values='valor',
        names='categoria',
        title='Despesas por Categoria',
        hole=0.3
    )

    g_3 = px.pie(
        ganhos_categoria,
        values='valor',
        names='categoria',
        title='Receita por categoria',
        hole=0.3
    )

    g_1_html = plot(g_1, output_type='div', include_plotlyjs='cdn')
    g_2_html = plot(g_2, output_type='div', include_plotlyjs='cdn')
    g_3_html = plot(g_3, output_type='div', include_plotlyjs='cdn')

    #Pra mandar transações pro template de dados
    transacoes = Transacao.objects.all()

    # =====================================================
    # 13. CONTEXTO ENVIADO PARA O TEMPLATE
    # =====================================================
    context = {
        'meses': MESES,
        'mes_selecionado': mes_selecionado,
        'anos_disponiveis': anos_disponiveis,
        'ano_selecionado': ano_selecionado,

        'receita_mes': receita_mes,
        'despesa_mes': despesa_mes,
        'saldo_mes': saldo_mes,

        'mes_maior_receita': mes_maior_receita,
        'valor_maior_receita': valor_maior_receita,
        'mes_maior_despesa': mes_maior_despesa,
        'valor_maior_despesa': valor_maior_despesa,

        'transacoes': transacoes,

        'g_1': g_1_html,
        'g_2': g_2_html,
        'g_3': g_3_html,
    }

    return render(request, 'analytics/dados.html', context)
