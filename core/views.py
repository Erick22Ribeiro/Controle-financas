from django.shortcuts import render, redirect
from core.models import Transacao, Categoria, Conta

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
            categoria = request.POST.get('categoria')
            conta = request.POST.get('conta')
            obs = request.POST.get('observacoes')

            Transacao.objects.create(
                descricao = descricao,
                valor = valor,
                data = data,
                categoria = categoria,
                conta = conta,
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



    categorias = Categoria.objects.all()

    context = {
        'categorias': categorias
    }

    return render(request, 'core/home.html', context)