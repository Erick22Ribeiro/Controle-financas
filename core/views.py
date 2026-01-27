from django.shortcuts import render, redirect, get_object_or_404
from core.models import Transacao, Categoria, Conta
import sqlite3
from datetime import date
from django.db.models import Sum
from django.db.models.functions import ExtractYear


import pandas as pd #analise
import plotly.express as px #exibição
from plotly.offline import plot
from django.http import HttpResponse

# Create your views here.
def financas(request):

    if request.method == 'POST':

        #pega o valor do input hidden, pra especificar nas consições
        tipo_form = request.POST.get('tipo_form')

        #Adicionar TransaçÃo
        if tipo_form == 'transacao':

            descricao = request.POST.get('descricao_t')
            valor = request.POST.get('valor')
            data = request.POST.get('data')
            categoria_id = request.POST.get('categoria')
            conta_id = request.POST.get('nome_conta')
            obs = request.POST.get('observacoes')

            Transacao.objects.create(
                descricao = descricao,
                valor = valor,
                data = data,
                categoria_id = categoria_id,
                conta_id = conta_id,
                observacao = obs,
            )

            return redirect('home')
        

        #Adicionar Categoria
        elif tipo_form == 'categoria':

            nome = request.POST.get('nome_cat')
            descricao = request.POST.get('descricao_cat')
            tipo = request.POST.get('tipo')

            Categoria.objects.create(
                nome = nome,
                descricao = descricao,
                tipo = tipo,
            )

            return redirect('home')


        #Adicionar Conta
        elif tipo_form == 'contas':

            nome = request.POST.get('nome_conta')
            saldo_inicial = request.POST.get('saldo_inicial')

            Conta.objects.create(
                nome = nome,
                saldo_inicial = saldo_inicial
            )

            return redirect('home')
        
        #Editar categoria
        elif tipo_form == 'editar_categoria':

            categoria_id = request.POST.get('categoria_id')
            novo_nome = request.POST.get('novo_nome')
            novo_tipo = request.POST.get('novo_tipo')


            categoria = get_object_or_404(Categoria, id=categoria_id) #Pega a categoria da classe categoria cujo id é igual ao passado (categoria_id)

            categoria.nome = novo_nome
            categoria.tipo = novo_tipo
            categoria.save()

            return redirect('home')


        #Excluir categoria
        elif tipo_form == 'deletar_categorias':

            ids = request.POST.getlist('ids_para_deletar') #pega uma lista de valores

            Categoria.objects.filter(id__in=ids).delete() 

            return redirect('home')
        

        #Editar conta
        elif tipo_form == 'editar_conta':

            conta_id = request.POST.get('conta_id')
            novo_nome = request.POST.get('novo_nome_conta')
            novo_saldo_i = request.POST.get('novo_saldo_i')

            conta = get_object_or_404(Conta, id = conta_id)

            conta.nome = novo_nome
            conta.saldo_inicial = novo_saldo_i
            conta.save()

            return redirect('home')

        #Excluir conta
        elif tipo_form == 'deletar_contas':

            ids = request.POST.getlist('ids_para_deletar_conta')

            Conta.objects.filter(id__in=ids).delete() 

            return redirect('home')
        
        #Deletar Transação
        elif tipo_form == 'deletar_tran':

            ids = request.POST.getlist('ids_para_deletar_tran')

            Transacao.objects.filter(id__in=ids).delete() 

            return redirect('home')


    categorias = Categoria.objects.all()
    contas = Conta.objects.all()
    transacoes = Transacao.objects.all()

    context = {
        'categorias': categorias,
        'contas': contas,
        'transacoes': transacoes
    }

    return render(request, 'core/home.html', context)

 #======================== DADOS ================================

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

    return render(request, 'core/dados.html', context)
