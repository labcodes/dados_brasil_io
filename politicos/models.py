from django.db import models


class Partido(models.Model):
    sigla = models.CharField(max_length=15, primary_key=True)
    nome = models.CharField(max_length=255)
    deferimento = models.DateField()
    presidente_nacional = models.CharField(max_length=255)
    legenda = models.PositiveIntegerField()

    def __str__(self):
        return self.sigla


class Deputado(models.Model):
    id_camara = models.IntegerField()
    nome = models.CharField(max_length=255)
    partido = models.ForeignKey(Partido)
    uf = models.ForeignKey('comum.Estado')
    id_legislatura = models.IntegerField()

    def __str__(self):
        return f'{self.nome} - {self.partido_id}'

