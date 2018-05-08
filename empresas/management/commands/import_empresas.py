import bisect
from datetime import datetime
import pandas as pd
from django.core.management import BaseCommand
from django.db import transaction

from empresas.models import Empresa

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('csv', type=str)
        parser.add_argument('uf', type=str)
        parser.add_argument('inicio', type=int)

    def handle(self, *args, **options):
        uf = options['uf']
        log = open(f'{uf}_EMPRESAS_LOG.txt', 'w')

        cnpjs_salvos = sorted(Empresa.objects.values_list('cnpj', flat=True))

        log.write(f'{datetime.now().isoformat()}  Abrindo CSV para {uf}\n')
        csv = pd.read_csv(
            options['csv'],
            chunksize=100000,
            dtype={'cpf_cnpj_socio': str, 'cnpj_empresa': str}
        )

        for contador, grupo in enumerate(csv):
            if contador >= options.get('inicio', 0):
                log.write(f'{datetime.now().isoformat()}  Removendo duplicatas de empresas do grupo {contador} do {uf}\n')
                grupo = grupo.drop_duplicates(['cnpj_empresa'], keep='first')
                grupo = grupo[~grupo['cnpj_empresa'].isin(cnpjs_salvos)]

                log.write(f'{datetime.now().isoformat()}  Importando dados de empresas do grupo {contador} do {uf}\n')
                empresas = []
                for dados in grupo.itertuples():
                    empresas.append(Empresa(
                        cnpj=dados.cnpj_empresa,
                        nome=dados.nome_empresa,
                        uf_id=uf
                    ))
                    bisect.insort(cnpjs_salvos, dados.cnpj_empresa)

                log.write(f'{datetime.now().isoformat()}  Cirando Empresas do grupo {contador} do {uf}\n')
                Empresa.objects.bulk_create(empresas)

