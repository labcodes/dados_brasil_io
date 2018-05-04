import requests
from django.core.management import BaseCommand

from politicos.models import Partido

class Command(BaseCommand):

    def handle(self, *args, **options):
        partidos = []

        camara_url = 'https://dadosabertos.camara.leg.br/api/v2/partidos/?formato=json&itens=100'

        resposta = requests.get(camara_url).json()

        for partido in resposta['dados']:
            partidos.append(Partido(
                id_camara=partido['id'],
                nome=partido['nome'],
                sigla=partido['sigla'],
            ))

        Partido.objects.bulk_create(partidos)
