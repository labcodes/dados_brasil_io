from datetime import date
from rest_framework import generics

from politicos.filters import DeputadoFilter
from politicos.models import Deputado
from politicos.serializers import DeputadoSerializer


class DeputadoListView(generics.ListAPIView):
    serializer_class = DeputadoSerializer
    filterset_class = DeputadoFilter

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
