import csv
import rows
from django.core.management import BaseCommand
from django.db import transaction

from empresas.models import Socio, Empresa

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('csv', type=str)

    def handle(self, *args, **options):
        dados = open(options['csv'])
        log = open('SOCIOS_LOG.txt', 'w')
        log_cnpjs_invalidos = open('CNPJS_INVALIDOS.txt', 'w')

        empresas = []
        socios = []
        cnpjs_adicionados = []

        reader = csv.DictReader(dados)

        todos_cnpjs = set([r['cnpj_empresa'] for r in reader if r.get('cnpj_empresa')])

        dados.seek(0)
        reader = csv.DictReader(dados)
        cnpjs_socios = set(r['cpf_cnpj_socio'] for r in reader if r.get('cpf_cnpj_socio'))

        cnpjs_invalidos = cnpjs_socios - todos_cnpjs

        dados.seek(0)
        reader = csv.DictReader(dados)
        for counter, row in enumerate(reader):
            if row.get('cnpj_empresa'):

                # Empresas
                if not row.get('cnpj_empresa') in cnpjs_adicionados:

                    cnpjs_adicionados.append(row['cnpj_empresa'])
                    empresas.append(Empresa(
                        cnpj=row['cnpj_empresa'],
                        nome=row.get('nome_empresa'),
                        unidade_federativa=row.get('unidade_federativa')
                    ))

                # Socios

                ## Validação empresa origem
                cnpj_socio = row.get('cpf_cnpj_socio')
                if cnpj_socio and cnpj_socio in cnpjs_invalidos:
                    log_cnpjs_invalidos.write(','.join(row.values()) + '\n')
                    cnpj_socio = None
                cnpj_socio = cnpj_socio if not cnpj_socio == '' else None

                socios.append(Socio(
                    nome=row.get('nome_socio'),
                    empresa_origem_id=cnpj_socio,
                    tipo_socio=row.get('codigo_tipo_socio'),
                    qualificacao_socio=row.get('codigo_qualificacao_socio'),
                    empresa_id=row['cnpj_empresa'],
                ))

            else:
                log.write(','.join(row.values()) + '\n')

        Empresa.objects.bulk_create(empresas)
        Socio.objects.bulk_create(socios)
