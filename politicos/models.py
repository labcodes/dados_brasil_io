from django.db import models


class Partido(models.Model):
    sigla = models.CharField(max_length=15, primary_key=True)
    nome = models.CharField(max_length=255)
    id_camara = models.IntegerField()

    def __str__(self):
        return self.sigla


class Deputado(models.Model):
    id_camara = models.IntegerField()
    nome = models.CharField(max_length=255)
    partido = models.ForeignKey(Partido, on_delete=models.PROTECT)
    uf = models.ForeignKey('comum.Estado', on_delete=models.PROTECT)
    id_legislatura = models.IntegerField()

    def __str__(self):
        return f'{self.nome} - {self.partido_id}'

