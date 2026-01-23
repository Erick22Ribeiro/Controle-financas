from django.shortcuts import render, redirect
from core.models import Transacao, Categoria, Conta
import sqlite3

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

import pandas as pd
from django.http import HttpResponse

def dados(request):

    #select_related -> otimiza queries
    transacoes = Transacao.objects.select_related('categoria', 'conta').values(
        'descricao', 'valor', 'data',
        'categoria__nome', 'categoria__tipo', 'conta__nome'
    )
    
    #Tratamento
    # Converter para DataFrame
    df = pd.DataFrame(list(transacoes))

    df.rename(columns={
        'categoria__nome': 'categoria',
        'categoria__tipo': 'tipo',
        'conta__nome': 'conta'
        }, inplace=True) #inplace=True precisa pra aparecer
    

    #Análise
    total_receitas = df[df['tipo'] == 'receita']['valor'].sum()

    context = {
        'total_receitas': total_receitas,
    }
    
    return render(request, 'core/dados.html', context)

