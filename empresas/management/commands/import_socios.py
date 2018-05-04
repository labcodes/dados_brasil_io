from datetime import datetime
import pandas as pd
import csv
from django.core.management import BaseCommand
from django.db import transaction

from empresas.models import Socio, Empresa

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('csv', type=str)
        parser.add_argument('inicio', type=int)

    def handle(self, *args, **options):
        log = open('SOCIOS_LOG.txt', 'w')

        cnpjs_adicionados = list(Empresa.objects.values_list('cnpj', flat=True))

        inicio = options.get('inicio', 0)

        print(f'{datetime.now().isoformat()}  Abrindo CSV')
        csv = pd.read_csv(
            options['csv'],
            chunksize=10000,
            dtype={'cpf_cnpj_socio': str, 'cnpj_empresa': str}
        )

        for contador, grupo in enumerate(csv):
            if contador >= inicio:
                print(f'Importando dados do grupo {contador}')
                empresas = []
                socios = []
                for indice, dados in enumerate(grupo.itertuples()):

                    # Empresas
                    if not dados.cnpj_empresa in cnpjs_adicionados:

                        cnpjs_adicionados.append(dados.cnpj_empresa)
                        empresas.append(Empresa(
                            cnpj=dados.cnpj_empresa,
                            nome=dados.nome_empresa,
                        ))

                    # Socios
                    socios.append(Socio(
                        nome=dados.nome_socio,
                        cpf_cnpj_socio=dados.cpf_cnpj_socio,
                        tipo_socio=dados.codigo_tipo_socio,
                        qualificacao_socio=dados.codigo_qualificacao_socio,
                        empresa_id=dados.cnpj_empresa,
                    ))

                with transaction.atomic():
                    print(f'{datetime.now().isoformat()}  Cirando Empresas')
                    Empresa.objects.bulk_create(empresas)
                    print(f'{datetime.now().isoformat()}  Cirando Socios')
                    Socio.objects.bulk_create(socios)
