from datetime import datetime
import pandas as pd
from django.core.management import BaseCommand
from django.db import transaction

from empresas.models import Empresa, Sociedade

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('csv', type=str)
        parser.add_argument('uf', type=str)
        parser.add_argument('inicio', type=int)

    def handle(self, *args, **options):
        uf = options['uf']
        log = open(f'{uf}_PJ_LOG.txt', 'w')
        cnpjs_nao_registrados = open(f'INVALIDOS_LOG.txt', 'a')

        log.write(f'{datetime.now().isoformat()}  Abrindo CSV para PJ\n')
        csv = pd.read_csv(
            options['csv'],
            chunksize=100000,
            dtype={'cpf_cnpj_socio': str, 'cnpj_empresa': str}
        )
        cnpjs_salvos = sorted(Empresa.objects.values_list('cnpj', flat=True))

        for contador, grupo in enumerate(csv):
            if contador >= options.get('inicio', 0):
                log.write(f'{datetime.now().isoformat()}  Filtrando socios PJ do grupo {contador}\n')
                grupo = grupo[grupo['codigo_tipo_socio'] == 1]
                sociedades = []

                log.write(f'{datetime.now().isoformat()}  Criando empresas com cnpj invalido do grupo {contador}\n')
                invalidos = grupo[~grupo['cpf_cnpj_socio'].isin(cnpjs_salvos)]
                for dados in invalidos.itertuples():
                    cnpjs_nao_registrados.write(f'{dados.cpf_cnpj_socio};{dados.nome_socio};{uf};{dados.cnpj_empresa};{dados.nome_empresa}]')
                invalidos = invalidos.drop_duplicates(['cpf_cnpj_socio'])
                empresas_invalidas = []
                for dados in invalidos.itertuples():
                    empresas_invalidas.append(Empresa(
                        nome=f'INVALIDO {dados.nome_socio}',
                        cnpj=dados.cpf_cnpj_socio,
                        uf_id=uf,
                    ))
                    cnpjs_salvos.append(dados.cpf_cnpj_socio)
                Empresa.objects.bulk_create(empresas_invalidas)

                log.write(f'{datetime.now().isoformat()}  Importando sociedades do grupo {contador}\n')
                for dados in grupo.itertuples():
                    sociedades.append(Sociedade(
                        tipo_socio=1,
                        qualificacao_socio=dados.codigo_qualificacao_socio,
                        empresa_id=dados.cnpj_empresa,
                        socio_pessoa_juridica_id=dados.cpf_cnpj_socio
                    ))
                log.write(f'{datetime.now().isoformat()}  Cirando Sociedades do grupo {contador}\n')
                Sociedade.objects.bulk_create(sociedades)
        log.write(f'{datetime.now().isoformat()}  Importação finalizada\n')

