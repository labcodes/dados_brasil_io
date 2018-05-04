import csv
import rows
from django.core.management import BaseCommand
from django.db import transaction
from dados.models import Socio, Empresa

class Command(BaseCommand):

    def handle(self, *args, **options):
        dados = open('../socios-brasil/output/Brasil.csv')
        log = open('SOCIOS_LOG.txt')

        reader = csv.DictReader(dados)
        for counter, row in enumerate(reader):
            try:
                with transaction.atomic():
                    empresa, _ = Empresa.objects.get_or_create(
                        cnpj=row['cnpj_empresa'],
                        nome=row['nome_empresa'],
                        unidade_federativa=row['unidade_federativa']
                    )
                    socio = Socio.objects.create(
                        nome=row['nome_socio'],
                        cnpj=row['cpf_cnpj_socio'],
                        tipo_socio=row['codigo_tipo_socio'],
                        qualificacao_socio=row['codigo_qualificacao_socio'],
                        empresa=empresa,
                    )
                    print(str(counter * 100 / 17780861) + '%')
            except Exception:
                log.write(str(counter) + ','.join(row.items()))

