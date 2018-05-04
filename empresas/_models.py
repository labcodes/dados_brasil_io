from django.db import models


class GastosDeputados(models.Model):
    # Deputado
    codlegislatura = models.IntegerField(null=True)
    # Gasto
    datemissao = models.DateTimeField(null=True)
    idedocumento = models.IntegerField(null=True)
    idecadastro = models.IntegerField(null=True)
    indtipodocumento = models.IntegerField(null=True)
    # Deputado
    nucarteiraparlamentar = models.IntegerField(null=True)
    nudeputadoid = models.IntegerField(null=True)
    nulegislatura = models.IntegerField(null=True)
    # Gasto
    numano = models.IntegerField(null=True)
    numespecificacaosubcota = models.IntegerField(null=True)
    numlote = models.IntegerField(null=True)
    nummes = models.IntegerField(null=True)
    numparcela = models.IntegerField(null=True)
    numressarcimento = models.IntegerField(null=True)
    numsubcota = models.IntegerField(null=True)
    # Deputado
    sgpartido = models.CharField(max_length=18, null=True)
    sguf = models.CharField(max_length=2, null=True)
    txnomeparlamentar = models.CharField(max_length=63, null=True)
    # Gasto
    txtcnpjcpf = models.CharField(max_length=14, null=True)
    txtdescricao = models.CharField(max_length=127, null=True)
    txtdescricaoespecificacao = models.CharField(max_length=31, null=True)
    txtfornecedor = models.CharField(max_length=255, null=True)
    txtnumero = models.CharField(max_length=63, null=True)
    txtpassageiro = models.CharField(max_length=63, null=True)
    txttrecho = models.CharField(max_length=127, null=True)
    vlrdocumento = models.DecimalField(null=True, max_digits=8, decimal_places=2)
    vlrglosa = models.DecimalField(null=True, max_digits=8, decimal_places=2)
    vlrliquido = models.DecimalField(null=True, max_digits=8, decimal_places=2)
    vlrrestituicao = models.DecimalField(null=True, max_digits=8, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=['-datemissao']),
            models.Index(fields=['datemissao']),
            models.Index(fields=['idedocumento']),
            models.Index(fields=['numressarcimento']),
            models.Index(fields=['sgpartido']),
            models.Index(fields=['sguf']),
            models.Index(fields=['txnomeparlamentar']),
            models.Index(fields=['txtcnpjcpf']),
            models.Index(fields=['txtdescricao']),
            models.Index(fields=['txtdescricaoespecificacao']),
            models.Index(fields=['txtfornecedor']),
            models.Index(fields=['vlrliquido']),
        ]
        ordering = ['-datemissao']


class SalariosMagistrados(models.Model):
    # Magistrado
    lotacao = models.CharField(max_length=255, null=True)
    cargo = models.CharField(max_length=63, null=True)
    cpf = models.CharField(max_length=11, null=True)
    # Salario
    data_de_publicacao = models.DateField(null=True)
    descontos_diversos = models.DecimalField(max_digits=12, null=True, decimal_places=2)
    diarias = models.DecimalField(max_digits=12, null=True, decimal_places=2)
    direitos_eventuais = models.DecimalField(max_digits=12, null=True, decimal_places=2)
    direitos_pessoais = models.DecimalField(max_digits=12, null=True, decimal_places=2)
    imposto_de_renda = models.DecimalField(max_digits=12, null=True, decimal_places=2)
    indenizacoes = models.DecimalField(max_digits=12, null=True, decimal_places=2)
    mesano_de_referencia = models.DateField(null=True)
    # Magistrado
    nome = models.CharField(max_length=63, null=True)
    orgao = models.CharField(max_length=63, null=True)
    # Salario
    previdencia_publica = models.DecimalField(max_digits=12, null=True, decimal_places=2)
    remuneracao_do_orgao_de_origem = models.DecimalField(max_digits=12, null=True, decimal_places=2)
    rendimento_liquido = models.DecimalField(max_digits=12, null=True, decimal_places=2)
    retencao_por_teto_constitucional = models.DecimalField(max_digits=12, null=True, decimal_places=
    2)
    subsidio = models.DecimalField(max_digits=12, null=True, decimal_places=2)
    total_de_descontos = models.DecimalField(max_digits=12, null=True, decimal_places=2)
    total_de_rendimentos = models.DecimalField(max_digits=12, null=True, decimal_places=2)
    tribunal = models.CharField(max_length=127, null=True)
    url = models.CharField(max_length=2000, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['cargo']),
            models.Index(fields=['mesano_de_referencia']),
            models.Index(fields=['nome']),
            models.Index(fields=['orgao']),
            models.Index(fields=['rendimento_liquido']),
            models.Index(fields=['retencao_por_teto_constitucional']),
            models.Index(fields=['total_de_rendimentos']),
            models.Index(fields=['tribunal']),
        ]
        ordering = ['tribunal', 'nome']


class SociosBrasil(models.Model):
    # Empresa
    cnpj_empresa = models.CharField(max_length=14, null=True)
    nome_empresa = models.CharField(max_length=255, null=True)
    codigo_tipo_socio = models.IntegerField(null=True)
    tipo_socio = models.CharField(max_length=15, null=True)
    # Socio
    cpf_cnpj_socio = models.CharField(max_length=14, null=True)
    # Empresa
    codigo_qualificacao_socio = models.IntegerField(null=True)
    qualificacao_socio = models.CharField(max_length=127, null=True)
    # Socio
    nome_socio = models.CharField(max_length=255, null=True)
    # Empresa
    unidade_federativa = models.CharField(max_length=2, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['cnpj_empresa']),
            models.Index(fields=['nome_empresa']),
            models.Index(fields=['nome_socio']),
            models.Index(fields=['unidade_federativa']),
        ]
        ordering = ['cnpj_empresa', 'nome_socio']


class GastosDiretos(models.Model):
    ano = models.IntegerField(null=True)
    codigo_acao = models.CharField(max_length=4, null=True)
    codigo_elemento_despesa = models.IntegerField(null=True)
    codigo_favorecido = models.CharField(max_length=112, null=True)
    codigo_funcao = models.IntegerField(null=True)
    codigo_grupo_despesa = models.IntegerField(null=True)
    codigo_orgao = models.IntegerField(null=True)
    codigo_orgao_superior = models.IntegerField(null=True)
    codigo_programa = models.IntegerField(null=True)
    codigo_subfuncao = models.IntegerField(null=True)
    codigo_unidade_gestora = models.IntegerField(null=True)
    data_pagamento = models.DateField(null=True)
    data_pagamento_original = models.CharField(max_length=112, null=True)
    gestao_pagamento = models.CharField(max_length=112, null=True)
    linguagem_cidada = models.CharField(max_length=199, null=True)
    mes = models.IntegerField(null=True)
    nome_acao = models.CharField(max_length=247, null=True)
    nome_elemento_despesa = models.CharField(max_length=113, null=True)
    nome_favorecido = models.CharField(max_length=208, null=True)
    nome_funcao = models.CharField(max_length=21, null=True)
    nome_grupo_despesa = models.CharField(max_length=25, null=True)
    nome_orgao = models.CharField(max_length=45, null=True)
    nome_orgao_superior = models.CharField(max_length=45, null=True)
    nome_programa = models.CharField(max_length=110, null=True)
    nome_subfuncao = models.CharField(max_length=50, null=True)
    nome_unidade_gestora = models.CharField(max_length=45, null=True)
    numero_documento = models.CharField(max_length=112, null=True)
    valor = models.DecimalField(max_digits=18, null=True, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(['-data_pagamento']),
            models.Index(['codigo_favorecido']),
            models.Index(['nome_elemento_despesa']),
            models.Index(['nome_favorecido']),
            models.Index(['nome_funcao']),
            models.Index(['nome_grupo_despesa']),
            models.Index(['nome_orgao_superior']),
            models.Index(['nome_subfuncao']),
            models.Index(['nome_unidade_gestora']),
            models.Index(['valor']),
        ]
        ordering = ['-data_pagamento', 'nome_favorecido']


