from django.contrib import admin
from dashboard.models import Cidade, Colaborador, Responsavel

from import_export.admin import ImportExportModelAdmin
from import_export import resources

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

    resource_class = CidadeResource


class ColaboradorAdmin(ImportExportModelAdmin):
    def lista_cidades(self,obj):
        return [c for c in obj.colaboradores_cidade.all()]

    lista_cidades.short_description = 'Territórios'

    search_fields = ('nome',)
    list_filter = ('tipo','colaboradores_cidade')
    list_display = ('nome', 'tel', 'tipo', 'lista_cidades')

    resource_class = ColaboradorResource

admin.site.site_header = 'ZéGustavo 1819 Dashboard'
admin.site.register(Cidade, CidadeAdmin)
admin.site.register(Colaborador, ColaboradorAdmin)
admin.site.register(Responsavel)
