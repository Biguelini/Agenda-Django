from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Contato
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages

# Create your views here.
def index(request):
    
    
    
    contatos = Contato.objects.order_by('nome').filter(mostrar=True)
    paginator = Paginator(contatos, 5) 
    
    page = request.GET.get('p')
    contatos = paginator.get_page(page)
    
    return render(request, 'contatos/index.html', {
        'contatos':contatos
    })
def ver_contato(request, contato_id):
    try:
        contato = Contato.objects.get(id=contato_id)
        if not contato.mostrar:
            messages.add_message(request, messages.ERROR, 'O contato não pode ser mostrado')
            return redirect('index')
        return render(request, 'contatos/ver_contato.html', {
            'contato':contato
        })
    except Contato.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'O contato não existe!')
        return redirect('index')
        
def busca(request):
    termo = request.GET.get('termo')
    if termo is None:
        messages.add_message(request, messages.ERROR, 'O campo busca não pode ficar vazio!')
        return redirect('index')
        
    campos = Concat('nome',Value(' '), 'sobrenome')
    contatos = Contato.objects.annotate(nome_completo=campos).filter(Q(nome_completo__icontains=termo) | Q(telefone__icontains=termo))
    
    messages.add_message(request, messages.SUCCESS, f'Retornando {len(contatos)} resultados')
    
    paginator = Paginator(contatos, 5) 
    page = request.GET.get('p')
    contatos = paginator.get_page(page)
    return render(request, 'contatos/busca.html', {
        'contatos':contatos
    })