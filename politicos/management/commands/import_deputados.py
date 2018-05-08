import requests
from django.core.management import BaseCommand

from politicos.models import Deputado

class Command(BaseCommand):

    def pega_proxima_pagina(self, resposta):
        tem_proxima_pagina = [
            link['href'] for link in resposta['links']
            if link['rel'] == 'next'
        ]
        return tem_proxima_pagina and tem_proxima_pagina[0]


    def handle(self, *args, **options):
        deputados = []

        camara_url = 'https://dadosabertos.camara.leg.br/api/v2/deputados/?formato=json&itens=100'

        resposta = requests.get(camara_url).json()

        proxima_pagina = self.pega_proxima_pagina(resposta)

        while proxima_pagina:
            for deputado in resposta['dados']:
                deputados.append(Deputado(
                    id=deputado['id'],
                    nome=deputado['nome'],
                    partido_id=deputado['siglaPartido'],
                    uf_id=deputado['siglaUf'],
                    id_legislatura=deputado['idLegislatura']
                ))

            resposta = requests.get(proxima_pagina).json()
            proxima_pagina = self.pega_proxima_pagina(resposta)

        Deputado.objects.bulk_create(deputados)
