from django.db import models


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
    )

    def __str__(self):
        return f'{self.valor_documento} {self.mes}/{self.ano}'

    class Meta:
        # indexes = [
        #     models.Index(fields=['-data_emissao']),
        #     models.Index(fields=['data_emissao']),
        #     models.Index(fields=['id_documento']),
        #     models.Index(fields=['ressarcimento']),
        #     models.Index(fields=['cpf']),
        #     models.Index(fields=['descricao']),
        #     models.Index(fields=['descricao_especificacao']),
        #     models.Index(fields=['fornecedor']),
        #     models.Index(fields=['valor_liquido']),
        #     models.Index(fields=['valor_documento']),
        #     models.Index(fields=['deputado']),
        #     models.Index(fields=['empresa']),
        # ]
        ordering = ['-data_emissao']
