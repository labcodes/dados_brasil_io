from rest_framework import generics

from politicos.filters import DeputadoFilter
from politicos.models import Deputado
from politicos.serializers import DeputadoSerializer, DeputadoGastosSerializer


class DeputadoListView(generics.ListAPIView):
    serializer_class = DeputadoSerializer
    filterset_class = DeputadoFilter
    queryset = Deputado.objects.all().select_related(
        'partido', 'uf'
    )


class DeputadoGastosView(generics.ListAPIView):
    serializer_class = DeputadoGastosSerializer
    filterset_class = DeputadoFilter
    queryset = Deputado.objects.all().select_related(
        'partido', 'uf'
    ).prefetch_related('gastos__empresa')
