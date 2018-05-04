from django.core.management import BaseCommand

from comum.models import Estado


class Command(BaseCommand):

    def handle(self, *args, **options):
        UNIDADES_FEDERATIVAS = (
            ('Acre', 'AC'),
            ('Alagoas', 'AL'),
            ('Amapá', 'AP'),
            ('Amazonas', 'AM'),
            ('Bahia', 'BA'),
            ('Ceará', 'CE'),
            ('Distrito Federal', 'DF'),
            ('Espírito Santo', 'ES'),
            ('Goiás', 'GO'),
            ('Maranhão', 'MA'),
            ('Mato Grosso', 'MT'),
            ('Mato Grosso do Sul', 'MS'),
            ('Minas Gerais', 'MG'),
            ('Paraná', 'PR'),
            ('Paraíba', 'PB'),
            ('Pará', 'PA'),
            ('Pernambuco', 'PE'),
            ('Piauí', 'PI'),
            ('Rio Grande do Norte', 'RN'),
            ('Rio Grande do Sul', 'RS'),
            ('Rio de Janeiro', 'RJ'),
            ('Rondônia', 'RO'),
            ('Roraima', 'RR'),
            ('Santa Catarina', 'SC'),
            ('Sergipe', 'SE'),
            ('São Paulo', 'SP'),
            ('Tocantins', 'TO'),
        )
        for unidade in UNIDADES_FEDERATIVAS:
            Estado.objects.create(sigla=unidade[1], nome=unidade[0])

