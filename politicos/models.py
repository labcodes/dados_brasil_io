from django.db import models


class Partido(models.Model):
    sigla = models.CharField(max_length=15)
    nome = models.CharField(max_length=255)
    deferimento = models.DateField()
    presidente_nacional = models.CharField(max_length=255)
    legenda = models.PositiveIntegerField()

    def __str__(self):
        return self.sigla

