from django.shortcuts import render
from .models import Cidade


def index(request):
    cidades = Cidade.objects.all()
    dados = {}
    for c in cidades:
        dados[c.ibge] = {
            "nome" : c.nome,
            "dobradas" : list(c.colaboradores.values())
        }

    context = { "dados" : dados}

    return render(request, 'dashboard/index.html', context)
