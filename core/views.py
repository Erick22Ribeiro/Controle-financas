from django.shortcuts import render, redirect
from core.models import Transacao, Categoria, Conta
import sqlite3

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
        

        #Excluir categoria
        elif tipo_form == 'deletar_categorias':

            ids = request.POST.getlist('ids_para_deletar') #pega uma lista de valores

            Categoria.objects.filter(id__in=ids).delete() 

            return redirect('home')


        #Excluir conta
        elif tipo_form == 'deletar_contas':

            ids = request.POST.getlist('ids_para_deletar_conta')

            Conta.objects.filter(id__in=ids).delete() 

            return redirect('home')
        
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



def dados(request):

    #select_related -> otimiza queries
    transacoes = Transacao.objects.select_related('categoria', 'conta').values(
        'descricao', 'valor', 'data',
        'categoria__nome', 'categoria__tipo', 'conta__nome'
    )
    
    #Tratamento ====================================

        # Converter para DataFrame
    df = pd.DataFrame(list(transacoes))

    df.rename(columns={
        'categoria__nome': 'categoria',
        'categoria__tipo': 'tipo',
        'conta__nome': 'conta'
        }, inplace=True) #inplace=True precisa pra aparecer
    
        #Converter pra datetime
    df['data'] = pd.to_datetime(df['data'])

    #print(df)
    
    #Análise =======================================

    #Total receita e despesa
    total_receitas = df[df['tipo'] == 'receita']['valor'].sum()
    total_despesas = df[df['tipo'] == 'despesa']['valor'].sum()

    #Receita x despesa / g_1
    df['mes'] = df['data'].dt.to_period('M').astype(str) #Criação da coluna mes

        
    resumo_mensal = (
        df.groupby(['mes', 'tipo'])['valor'] #Agrupar por mes e tipo
        .sum()
        .reset_index() #precisa
    )


    #Despesas por categoria / g_2
    despesas = df[df['tipo'] == 'despesa']
    gastos_categoria = despesas.groupby('categoria')['valor'].sum().reset_index()


    #Categorias mais caras / g_3
    receitas = df[df['tipo'] == 'receita']
    ganhos_categoria = receitas.groupby('categoria')['valor'].sum().reset_index()


    #Exibição
    """ 
    ✔ Receitas x Despesas (mensal)
    ✔ Despesas por categoria (donut)
    ✔ Evolução de despesas no tempo
    ✔ Saldo mensal
    ✔ Top categorias mais caras 
    """

    #Gráfico Receita X despesa / g_1
    g_1 = px.bar(
        resumo_mensal,
        x = 'mes', y = 'valor',
        color = 'tipo',
        title = 'Receitas X Despesas por mês'
    )

    #Gráfico Despesas por categoria / g_2
    g_2 = px.pie(
        gastos_categoria,
        values = 'valor',
        names = 'categoria',
        title = 'Despesas por Categoria',
        hole = 0.3  # Donut chart
    )

    #Gráfico Gnahos por categoria / g_3
    g_3 = px.pie(
        ganhos_categoria,
        values = 'valor',
        names = 'categoria',
        title = 'Receita por categoria',
        hole = 0.3
    )


    g_1_html = plot(g_1, output_type='div', include_plotlyjs='cdn')
    g_2_html = plot(g_2, output_type='div', include_plotlyjs='cdn')
    g_3_html = plot(g_3, output_type='div', include_plotlyjs='cdn')

    context = {
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'g_1': g_1_html,
        'g_2': g_2_html,
        'g_3': g_3_html
    }

    return render(request, 'core/dados.html', context)

