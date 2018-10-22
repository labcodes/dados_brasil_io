from django.db import models
from django.db.models import Avg, Case, Count, Exists, F, FilteredRelation, OuterRef, Prefetch, Q, Sum, Value, When
from django.db.models.functions import Coalesce


class DeputadoQuerySet(models.QuerySet):

    def annotate_gasto_mensal_por_deputado(self):
        meses = range(1, 13)
        anos = range(2009, 2019)
        annotations = {
            f'gastos_{ano}_{mes:02}': Sum(
                'gastos__valor_liquido',
                filter=Q(gastos__mes=mes, gastos__ano=ano)
            )
            for ano in anos for mes in meses
        }
        return self.annotate(**annotations)

    def annotate_gasto_no_mes_por_deputado(self, mes, ano):
        annotation = {
            f'gastos_{ano}_{mes:02}': Sum(
                'gastos__valor_liquido',
                filter=Q(gastos__mes=mes, gastos__ano=ano)
            )
        }
        return self.annotate(**annotation)

    def annotate_gasto_no_mes_por_deputado2(self, mes, ano):
        return self.annotate(
            gastos_filtrados=FilteredRelation(
                'gastos',
                condition=Q(gastos__mes=mes, gastos__ano=ano)
            )
        ).annotate(
            **{f'gastos_{ano}_{mes:02}': Sum('gastos_filtrados__valor_liquido')}
        )

    def get_media_mensal(self):
        meses = range(1, 13)
        anos = range(2009, 2019)
        aggregations = {
            f'media_{ano}_{mes:02}': Avg(f'gastos_{ano}_{mes:02}')
            for ano in anos for mes in meses
        }
        return self.annotate_gasto_mensal_por_deputado().aggregate(**aggregations)

    def prefetch_gastos(self, **kwargs):
        gastos_queryset = GastoCotaParlamentar.objects.select_related(
            'empresa'
        ).filter(**kwargs)
        prefetch = Prefetch('gastos', queryset=gastos_queryset)
        return self.prefetch_related(prefetch)

    def annotate_gastos_acima_dobro(self, descricao_gasto):
        media = GastoCotaParlamentar.objects.filter_descricao(descricao_gasto).media()
        acima_dobro = Q(gastos__descricao=descricao_gasto, gastos__valor_liquido__gt=media * 2)
        return self.annotate(
            qtd_gastos=Count('gastos', filter=Q(gastos__descricao=descricao_gasto)),
            qtd_acima_dobro=Coalesce(
                Sum(
                    Case(
                        When(
                            Q(gastos__valor_liquido__gt=media * 2, gastos__descricao=descricao_gasto),
                            then=Value(1)
                        ),
                        output_field=models.IntegerField()
                    )
                ),
                0
            )
        )

    def annotate_empresas(self):
        from empresas.models import Empresa
        empresas_qs = Empresa.objects.filter(
            sociedades__socio_pessoa_fisica__nome=OuterRef('nome'),
            uf=OuterRef('uf')
        )
        return self.annotate(
            empresas=Exists(empresas_qs)
        )


class GastoCotaParlamentarQuerySet(models.QuerySet):

    def filter_descricao(self, descricao):
        return self.filter(descricao=descricao)

    def media(self):
        return self.aggregate(media=Avg('valor_liquido'))['media']



class Partido(models.Model):
    sigla = models.CharField(max_length=15, primary_key=True)
    nome = models.CharField(max_length=255)
    id_camara = models.IntegerField()

    def __str__(self):
        return self.sigla


class Deputado(models.Model):
    nome = models.CharField(max_length=255)
    partido = models.ForeignKey(Partido, on_delete=models.PROTECT)
    uf = models.ForeignKey('comum.Estado', on_delete=models.PROTECT)
    id_legislatura = models.IntegerField()
    carteira_parlamentar = models.IntegerField(null=True)

    objects = DeputadoQuerySet.as_manager()

    def __str__(self):
        return f'{self.nome} - {self.partido_id}'


class GastoCotaParlamentar(models.Model):
    TIPOS_DOCUMENTO = (
        (0, 'Nota Fiscal'),
        (1, 'Recibo'),
        (2, 'Despesa no Exterior'),
    )
    legislatura = models.IntegerField(null=True)
    data_emissao = models.DateTimeField(null=True)
    id_documento = models.IntegerField(null=True)
    tipo_documento = models.IntegerField(choices=TIPOS_DOCUMENTO, null=True)
    ano = models.IntegerField(null=True)
    especificacao_subcota = models.IntegerField(null=True)
    lote = models.IntegerField(null=True)
    mes = models.IntegerField(null=True)
    parcela = models.IntegerField(null=True)
    ressarcimento = models.IntegerField(null=True)
    subcota = models.IntegerField(null=True)
    cpf = models.CharField(max_length=14, null=True)
    descricao = models.CharField(max_length=127, null=True)
    descricao_especificacao = models.CharField(max_length=31, null=True)
    fornecedor = models.CharField(max_length=255, null=True)
    numero_documento = models.CharField(max_length=63, null=True)
    nome_passageiro = models.CharField(max_length=63, null=True)
    trecho_viagem = models.CharField(max_length=127, null=True)
    valor_documento = models.DecimalField(null=True, max_digits=8, decimal_places=2)
    valor_glosa = models.DecimalField(null=True, max_digits=8, decimal_places=2)
    valor_liquido = models.DecimalField(null=True, max_digits=8, decimal_places=2)
    valor_restituicao = models.DecimalField(null=True, max_digits=8, decimal_places=2)
    deputado = models.ForeignKey(
        Deputado,
        related_name='gastos',
        db_index=True,
        on_delete=models.PROTECT,
    )
    empresa = models.ForeignKey(
        'empresas.Empresa',
        related_name='gastos_deputados',
        db_index=True,
        on_delete=models.PROTECT,
        null=True,
    )

    objects = GastoCotaParlamentarQuerySet.as_manager()

    def __str__(self):
        return f'{self.valor_documento} {self.mes}/{self.ano}'

    class Meta:
        indexes = [
            models.Index(fields=['-data_emissao']),
            models.Index(fields=['data_emissao']),
            models.Index(fields=['mes']),
            models.Index(fields=['ano']),
            models.Index(fields=['descricao']),
            models.Index(fields=['descricao_especificacao']),
            models.Index(fields=['fornecedor']),
            models.Index(fields=['valor_liquido']),
            models.Index(fields=['valor_documento']),
            models.Index(fields=['deputado']),
            models.Index(fields=['empresa']),
        ]
        ordering = ['-data_emissao']
