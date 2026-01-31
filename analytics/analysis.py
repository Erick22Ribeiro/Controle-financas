from django.shortcuts import render
from core.models import Transacao
from datetime import date
from django.db.models import Sum
from django.db.models.functions import ExtractYear


import pandas as pd #analise
import plotly.express as px #exibição
from plotly.offline import plot 

#Função que calcula: Saldo total, Receita do mes e Despesa do mês
def resumo_financeiro():

    hoje = date.today() 
    mes_atual = hoje.month
    ano_atual = hoje.year

    #Total Receita do mês
    receita_mes = Transacao.objects.filter(
        categoria__tipo = 'receita',
        data__month = mes_atual,
        data__year = ano_atual,
    ).aggregate(total = Sum('valor'))['total'] or 0 

    #Despesas do mês
    despesa_mes = Transacao.objects.filter(
        categoria__tipo = 'despesa',
        data__month = mes_atual,
        data__year = ano_atual,
    ).aggregate(total = Sum('valor'))['total'] or 0 

    # Total de todas as receitas
    total_receita = Transacao.objects.filter(
        categoria__tipo = 'receita'
    ).aggregate(total = Sum('valor'))['total'] or 0 

    #Total de todas as despesas
    total_despesa = Transacao.objects.filter(
        categoria__tipo = 'despesa'
    ).aggregate(total = Sum('valor'))['total'] or 0

    saldo_total = total_receita - total_despesa

    return {
        'receita_mes': receita_mes,
        'despesa_mes': despesa_mes,
        'saldo_total': saldo_total,
    }
