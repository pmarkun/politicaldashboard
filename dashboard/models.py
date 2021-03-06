from django.db import models


SITUACAO_CHOICES = (
    (-2, 'emergencia!'),
    (-1, 'ruim'),
    (0, 'regular'),
    (1, 'bom'),
    (2, 'ótimo'),
)

PRIORIDADE_CHOICES = (
    ('BAIXA', 'Baixa'),
    ('MEDIA', 'Média'),
    ('ALTA', 'Alta'),
    ('ALTISSIMA', 'Altissima')
)

COLABORADOR_CHOICES = (
    ('CODEPUTADO', 'CoDeputado'),
    ('DOBRADA', 'Dobrada'),
    ('AGENTE', 'Agente Público'),
    ('MOBILIZA', 'Mobilizador'),
)

# Create your models here.
class Colaborador(models.Model):
    class Meta():
        verbose_name_plural = "Colaboradores"

    nome = models.CharField(max_length=200)
    tel = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    tipo = models.CharField(max_length=10, choices=COLABORADOR_CHOICES,default=None)
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, default=0)
    obs = models.TextField(blank=True)
    foto = models.ImageField(upload_to='colaboradores', blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)

    def __str__(self):
        return self.nome

class Cidade(models.Model):
    nome = models.CharField(max_length=200)
    ibge = models.CharField(max_length=200, blank=True)
    pop = models.IntegerField(default=0)
    ra = models.CharField(max_length=200, blank=True)
    rg = models.CharField(max_length=200, blank=True)
    projecao = models.IntegerField(blank=True, null=True)
    votos = models.IntegerField(default=0)
    votos_marina = models.IntegerField(default=0)
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, default='BAIXA')
    situacao_digital = models.IntegerField(choices=SITUACAO_CHOICES,default=0)
    situacao_territorio = models.IntegerField(choices=SITUACAO_CHOICES,default=0)
    colaboradores = models.ManyToManyField(Colaborador, related_name='colaboradores_cidade', blank=True)

    def __str__(self):
        return self.nome + " (" + str(self.projecao) + ")"

class Responsavel(models.Model):
    email = models.EmailField()
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class CidadeMap(Cidade):
    class Meta():
        proxy = True
        verbose_name = "Mapa de Território"
        verbose_name_plural = "Mapa de Territórios"


class Territorio(models.Model):
    nome = models.CharField(max_length=300)
    eleitores = models.IntegerField(blank=True)
    projecao = models.IntegerField(blank=True)
    cidades = models.ManyToManyField(Cidade, related_name='cidades_territorio', blank=True)
    situacao_territorio = models.IntegerField(choices=SITUACAO_CHOICES,default=0)

class Agenda(models.Model):
    nome = models.CharField(max_length=300, blank=True)
    cidades = models.ManyToManyField(Cidade, blank=True)
    data = models.DateField(blank=True)
    projecao = models.IntegerField(blank=True, null=True)
    realidade = models.IntegerField(blank=True, null=True)
    obs = models.TextField(blank=True)
