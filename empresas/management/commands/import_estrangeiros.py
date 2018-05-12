import bisect
from datetime import datetime
import pandas as pd
import numpy as np
import csv
from django.core.management import BaseCommand
from django.db import transaction

from empresas.models import Estrangeiro, Sociedade

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('csv', type=str)
        parser.add_argument('inicio', type=int)

    def handle(self, *args, **options):
        log = open('ESTRANGEIROS_LOG.txt', 'w')

        log.write(f'{datetime.now().isoformat()}  Abrindo CSV\n')
        csv = pd.read_csv(
            options['csv'],
            chunksize=100000,
            dtype={'cpf_cnpj_socio': str, 'cnpj_empresa': str}
        )

        for contador, grupo in enumerate(csv):
            if contador >= options.get('inicio', 0):
                log.write(f'{datetime.now().isoformat()}  Filtrando socios estrangeiros do grupo {contador}\n')
                grupo = grupo[grupo['codigo_tipo_socio'] == 3]
                sociedades = []
                log.write(f'{datetime.now().isoformat()}  Inserindo dados de estrangeiros do grupo {contador}\n')
                for dados in grupo.itertuples():
                    estrangeiro = Estrangeiro.objects.create(nome=dados.nome_socio)
                    sociedades.append(Sociedade(
                        tipo_socio=3,
                        qualificacao_socio=dados.codigo_qualificacao_socio,
                        empresa_id=dados.cnpj_empresa,
                        socio_estrangeiro=estrangeiro
                    ))
                log.write(f'{datetime.now().isoformat()}  Cirando Sociedades do grupo {contador}\n')
                Sociedade.objects.bulk_create(sociedades)

