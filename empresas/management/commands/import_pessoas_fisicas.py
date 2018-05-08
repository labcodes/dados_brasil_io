
from datetime import datetime
import pandas as pd
from django.core.management import BaseCommand
from django.db import transaction

from empresas.models import PessoaFisica, Sociedade

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('csv', type=str)
        parser.add_argument('uf', type=str)
        parser.add_argument('inicio', type=int)

    def handle(self, *args, **options):
        log = open('PF_LOG.txt', 'w')

        uf = options['uf']
        log.write(f'{datetime.now().isoformat()}  Abrindo CSV para {uf}\n')
        csv = pd.read_csv(
            options['csv'],
            chunksize=100000,
            dtype={'cpf_cnpj_socio': str, 'cnpj_empresa': str}
        )

        for contador, grupo in enumerate(csv):
            if contador >= options.get('inicio', 0):
                log.write(f'{datetime.now().isoformat()}  Filtrando socios PF do grupo {contador} do {uf}\n')
                grupo.loc(grupo['tipo_socio'] == 2)
                sociedades = []
                log.write(f'{datetime.now().isoformat()}  Inserindo dados de PF do grupo {contador} do {uf}\n')
                for dados in grupo.itertuples():
                    pessoa = PessoaFisica.objects.create(nome=dados.nome_socio)
                    sociedades.append(Sociedade(
                        tipo_socio=2,
                        qualificacao_socio=dados.codigo_qualificacao_socio,
                        empresa_id=dados.cnpj_empresa,
                        socio_pessoa_fisica=pessoa
                    ))
                log.write(f'{datetime.now().isoformat()}  Cirando Sociedades do grupo {contador} do {uf}\n')
                Sociedades.objects.bulk_create(sociedades)


