from django.db import models


class Estado(models.Model):
    sigla = models.CharField(max_length=2, primary_key=True)
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome
