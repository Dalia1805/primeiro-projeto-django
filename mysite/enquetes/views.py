
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Pergunta, Escolha
from django.shortcuts import render, get_object_or_404
from django.db.models import F

def index(request):
    ultimas_perguntas = Pergunta.objects.order_by('-data_publicacao')[:5]
    contexto = {'ultimas_perguntas': ultimas_perguntas }
    return render (request, 'enquetes/index.html',contexto)
def detalhes(request,pergunta_id):
    try:
        pergunta = Pergunta.objects.get(pk=pergunta_id)
    except:
        raise Http404('a pergunta não existe!')
    return render(request, 'enquetes/detalhes.html', {'pergunta': pergunta})
    
def resultados(request,pergunta_id):
    pergunta= get_object_or_404(pergunta, pk=pergunta_id)
    return render(request, "enquetes/resultados.html", {"pergunta": pergunta})
def votos(request,pergunta_id):
    pergunta= get_object_or_404(pergunta, pk=pergunta_id)
    try:
        escolha_selecionada = pergunta.escolha_set.get(pk=request.POST["esolha"])
    except (KeyError, Escolha.Doesnotexist):
        return render(
            "enquetes/detalhes.html",
            { 
                "question": pergunta,
                "error_message": "você não seliconou uma escolha.",
            },
        )
    else:
        escolha_selecionada.votos= F('votos') + 1
        escolha_selecionada.save()
        return HttpResponseRedirect(reverse("enquetes:resultados", args=(pergunta.id,)))