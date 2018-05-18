from datetime import date
from rest_framework import generics, serializers
from rest_framework.response import Response

from politicos.models import Deputado, GastoCotaParlamentar


class GastoCotaParlamentarSerializer(serializers.ModelSerializer):
    class Meta:
        model = GastoCotaParlamentar
        fields = '__all__'


class DeputadoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deputado
        fields = [
            'id', 'nome', 'partido', 'uf', 'id_legislatura',
            'gastos'
        ]
        depth = 2


class DeputadoListView(generics.ListAPIView):
    serializer_class = DeputadoSerializer

    def get_queryset(self):
        queryset = Deputado.objects.all().select_related('partido', 'uf')

        hoje = date.today()
        filtros = self.request.query_params.dict()
        filtros.setdefault('gastos_mes', hoje.month)
        filtros.setdefault('gastos_ano', hoje.year)

        queryset = queryset.prefetch_gastos(**{
            campo.replace('gastos_', ''): valor
            for campo, valor in filtros.items()
            if campo.startswith('gastos_')
        })

        return queryset
