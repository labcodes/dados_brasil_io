import rows
from dateutil.parser import parse
from django.core.management import BaseCommand

from politicos.models import Partido

class Command(BaseCommand):

    def handle(self, *args, **options):
        dados = rows.import_from_csv('partidos.csv')

        for row in dados:
            Partido.objects.create(
                sigla=row.sigla,
                nome=row.nome,
                deferimento=parse(row.deferimento, dayfirst=True),
                presidente_nacional=row.pres_nacional,
                legenda=row.no_da_legenda
            )

