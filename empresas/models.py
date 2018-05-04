from django.db import models


class Empresa(models.Model):
    cnpj = models.CharField(max_length=14, primary_key=True)
    nome = models.CharField(max_length=255, null=True, db_index=True)


class Socio(models.Model):
    TIPOS_SOCIO = (
        (1, 'Pessoa Jurídica'),
        (2, 'Pessoa Física'),
        (3, 'Nome Exterior'),
    )
    QUALIFICACOES_SOCIO = (
        (5, 'Administrador'),
        (8, 'Conselheiro de Administração'),
        (10, 'Diretor'),
        (16, 'Presidente'),
        (17, 'Procurador'),
        (20, 'Sociedade Consorciada'),
        (21, 'Sociedade Filiada'),
        (22, 'Sócio'),
        (23, 'Sócio Capitalista'),
        (24, 'Sócio Comanditado'),
        (25, 'Sócio Comanditário'),
        (26, 'Sócio de Indústria'),
        (28, 'Sócio-Gerente'),
        (29, 'Sócio Incapaz ou Relat.Incapaz (exceto menor)'),
        (30, 'Sócio Menor (Assistido/Representado)'),
        (31, 'Sócio Ostensivo'),
        (37, 'Sócio Pessoa Jurídica Domiciliado no Exterior'),
        (38, 'Sócio Pessoa Física Residente no Exterior'),
        (47, 'Sócio Pessoa Física Residente no Brasil'),
        (48, 'Sócio Pessoa Jurídica Domiciliado no Brasil'),
        (49, 'Sócio-Administrador'),
        (52, 'Sócio com Capital'),
        (53, 'Sócio sem Capital'),
        (54, 'Fundador'),
        (55, 'Sócio Comanditado Residente no Exterior'),
        (56, 'Sócio Comanditário Pessoa Física Residente no Exterior'),
        (57, 'Sócio Comanditário Pessoa Jurídica Domiciliado no Exterior'),
        (58, 'Sócio Comanditário Incapaz'),
        (59, 'Produtor Rural'),
        (63, 'Cotas em Tesouraria'),
        (65, 'Titular Pessoa Física Residente ou Domiciliado no Brasil'),
        (66, 'Titular Pessoa Física Residente ou Domiciliado no Exterior'),
        (67, 'Titular Pessoa Física Incapaz ou Relativamente Incapaz (exceto menor)'),
        (68, 'Titular Pessoa Física Menor (Assistido/Representado)'),
        (70, 'Administrador Residente ou Domiciliado no Exterior'),
        (71, 'Conselheiro de Administração Residente ou Domiciliado no Exterior'),
        (72, 'Diretor Residente ou Domiciliado no Exterior'),
        (73, 'Presidente Residente ou Domiciliado no Exterior'),
        (74, 'Sócio-Administrador Residente ou Domiciliado no Exterior'),
        (75, 'Fundador Residente ou Domiciliado no Exterior'),
    )

    nome = models.CharField(max_length=255, null=True, db_index=True)
    cpf_cnpj_socio = models.CharField(max_length=14, null=True, db_index=True)
    tipo_socio = models.PositiveSmallIntegerField(
        choices=TIPOS_SOCIO,
        null=True,
        db_index=True
    )
    qualificacao_socio = models.PositiveSmallIntegerField(
        choices=QUALIFICACOES_SOCIO,
        null=True
    )
    empresa = models.ForeignKey(
        Empresa,
        related_name='socios',
        null=True,
        on_delete=models.PROTECT,
        db_index=True
    )

