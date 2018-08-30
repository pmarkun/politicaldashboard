from django.contrib import admin
from dashboard.models import Cidade, Colaborador, Responsavel, CidadeMap, Territorio, Agenda
from django.shortcuts import render

from import_export.admin import ImportExportModelAdmin
from import_export import resources


class MyAdminSite(admin.AdminSite):
    def __init__(self, *args, **kwargs):
        super(MyAdminSite, self).__init__(*args, **kwargs)
        self._registry.update(admin.site._registry)

    def map(self, request):
        cidades = Cidade.objects.all()
        dados = {}
        for c in cidades:
            dados[c.ibge] = {
                "nome" : c.nome,
                "dobradas" : list(c.colaboradores.values())
            }

        context = { "dados" : dados}
        return render(request, 'dashboard/index.html', context)

    def get_urls(self):
        from django.conf.urls import url
        urls = super(MyAdminSite, self).get_urls()
        urls += [
            url(r'^map/$', self.admin_view(self.map))
        ]
        return urls

    def my_view(self, request):
        return HttpResponse("Hello!")

admin_site = MyAdminSite()

# Register your models here.

class CidadeResource(resources.ModelResource):

    class Meta():
        model = Cidade
        fields = ('id', 'ibge', 'nome', 'ra', 'rg','pop', 'votos',)

class ColaboradorResource(resources.ModelResource):

    class Meta():
        model = Colaborador
        fields = ('id', 'nome', 'tipo', 'obs')

class CidadeAdmin(ImportExportModelAdmin):
    def lista_colaboradores(self,obj):
        return ', '.join([c.nome + " ("+c.tipo+")" for c in obj.colaboradores.all()])

    lista_colaboradores.short_description = 'Colaboradores'

    search_fields = ('nome',)
    list_display = ('nome', 'pop', 'votos', 'prioridade', 'situacao_digital', 'situacao_territorio', 'lista_colaboradores')
    list_editable = ('situacao_digital','situacao_territorio')
    list_filter = ('prioridade', 'rg')
    filter_horizontal = ('colaboradores',)

    ordering = ('prioridade','-votos')

    resource_class = CidadeResource



class ColaboradorAdmin(ImportExportModelAdmin):
    def lista_cidades(self,obj):
        return [c for c in obj.colaboradores_cidade.all()]

    lista_cidades.short_description = 'Territórios'

    search_fields = ('nome',)

    list_filter = ('tipo','colaboradores_cidade')
    list_display = ('nome', 'tel', 'tipo', 'lista_cidades', 'prioridade', 'obs')
    list_editable = ('prioridade',)

    resource_class = ColaboradorResource


class CidadeMapAdmin(admin.ModelAdmin):
    change_list_template = 'dashboard/index.html'
    change_list_template = 'admin/cidademap_change_list.html'
    list_filter = ('colaboradores__tipo',)

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            qs = response.context_data["cl"].queryset
        except (AttributeError, KeyError):
            return response

        cidades = qs
        dados = {}
        for c in cidades:
            dados[c.ibge] = {
                "nome" : c.nome,
                "dobradas" : list(c.colaboradores.values())
            }
        response.context_data["dados"] = dados

        return response

admin_site.site_header = 'ZéGustavo 1819 Dashboard'
admin_site.register(Cidade, CidadeAdmin)
admin_site.register(CidadeMap, CidadeMapAdmin)
admin_site.register(Colaborador, ColaboradorAdmin)
admin_site.register(Responsavel)
admin_site.register(Territorio)
admin_site.register(Agenda)
