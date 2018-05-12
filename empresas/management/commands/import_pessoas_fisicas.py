from datetime import datetime
import pandas as pd
from django.core.management import BaseCommand
from django.db import transaction

from empresas.models import PessoaFisica, Sociedade

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('csv', type=str)
        parser.add_argument('inicio', type=int)

    def handle(self, *args, **options):
        log = open('PF_LOG.txt', 'w')

        log.write(f'{datetime.now().isoformat()}  Abrindo CSV\n')
        csv = pd.read_csv(
            options['csv'],
            chunksize=100000,
            dtype={'cpf_cnpj_socio': str, 'cnpj_empresa': str}
        )

        pessoa_id = 1
        for contador, grupo in enumerate(csv):
            if contador >= options.get('inicio', 0):
                log.write(f'{datetime.now().isoformat()}  Filtrando socios PF do grupo {contador}\n')
                grupo = grupo[grupo['codigo_tipo_socio'] == 2]
                sociedades = []
                pessoas = []
                log.write(f'{datetime.now().isoformat()}  Importando dados do grupo {contador}\n')
                for indice, dados in enumerate(grupo.itertuples()):
                    pessoas.append(PessoaFisica(nome=dados.nome_socio, id=pessoa_id))
                    sociedades.append(Sociedade(
                        tipo_socio=2,
                        qualificacao_socio=dados.codigo_qualificacao_socio,
                        empresa_id=dados.cnpj_empresa,
                        socio_pessoa_fisica_id=pessoa_id
                    ))
                    pessoa_id += 1
                log.write(f'{datetime.now().isoformat()}  Cirando PFs do grupo {contador}\n')
                PessoaFisica.objects.bulk_create(pessoas)
                log.write(f'{datetime.now().isoformat()}  Cirando Sociedades do grupo {contador}\n')
                Sociedade.objects.bulk_create(sociedades)

