from django.db import models
from django.db.models import Case, Count, Exists, F, OuterRef, Q, Subquery, Sum, Value, When
from django.db.models.functions import Coalesce


class EmpresaQuerySet(models.QuerySet):

    def annotate_deputados(self):
        from politicos.models import Deputado
        deputados_qs = Deputado.objects.values_list('nome', flat=True)
        return self.annotate(
            deputado=Subquery(
                deputados_qs.filter(
                    nome__in=OuterRef('sociedades__socio_pessoa_fisica__nome')
                )
            )
        )

    def annotate_deputados2(self):
        from politicos.models import Deputado
        deputados_qs = Deputado.objects.values_list('nome', flat=True)
        return self.annotate(
            deputado=Q(sociedades__socio_pessoa_fisica__nome__in=deputados_qs)
        )

    def annotate_graus_sociedades(self, grau):
        lookups = lambda x: '__'.join(['participacoes_sociedades__socio_pessoa_juridica'] * x)
        annotate_graus_sociedades = {
            f'grau_{n}': Coalesce(
                Sum(
                    Case(
                        When(
                            Q(**{f'{lookups(n)}__isnull': False})
                            &
                            ~Q(**{f'{lookups(n)}': F(f'{lookups(n - 1)}' if n - 1 else 'cnpj')})
                            &
                            ~Q(**{f'{lookups(n)}': F(f'{lookups(n - 2)}' if n - 2 > 0 else 'cnpj')}),
                            then=Value(1)
                        ),
                        output_field=models.IntegerField(),
                    )
                ),
                0,
            )
            for n in range(1, grau + 1)
        }
        return self.annotate(**annotate_graus_sociedades)

    def annotate_graus_sociedades2(self, grau):
        lookups = lambda x: '__'.join(['participacoes_sociedades__socio_pessoa_juridica'] * x)
        annotate_graus_sociedades = {
            f'grau_{n}': Count(
                Q(**{f'{lookups(n)}__isnull': False})
                &
                ~Q(**{f'{lookups(n)}': F(f'{lookups(n - 1)}' if n - 1 else 'cnpj')})
                &
                ~Q(**{f'{lookups(n)}': F(f'{lookups(n - 2)}' if n - 2 > 0 else 'cnpj')}),
                then=Value(1)
            )
            for n in range(1, grau + 1)
        }
        return self.annotate(**annotate_graus_sociedades)



class Empresa(models.Model):
    cnpj = models.CharField(max_length=14, primary_key=True)
    nome = models.CharField(max_length=255, null=True, db_index=True)
    uf = models.ForeignKey(
        'comum.Estado',
        db_index=True,
        related_name='empresas',
        on_delete=models.PROTECT,
    )

    objects = EmpresaQuerySet.as_manager()


class PessoaFisica(models.Model):
    nome = models.CharField(max_length=255, null=True, db_index=True)


class Estrangeiro(models.Model):
    nome = models.CharField(max_length=255, null=True, db_index=True)


class Sociedade(models.Model):
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
        related_name='sociedades',
        null=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    socio_pessoa_juridica = models.ForeignKey(
        Empresa,
        related_name='participacoes_sociedades',
        null=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    socio_pessoa_fisica = models.ForeignKey(
        PessoaFisica,
        related_name='participacoes_sociedades',
        null=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    socio_estrangeiro = models.ForeignKey(
        Estrangeiro,
        related_name='participacoes_sociedades',
        null=True,
        on_delete=models.PROTECT,
        db_index=True
    )
