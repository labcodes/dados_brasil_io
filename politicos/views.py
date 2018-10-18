from rest_framework import generics

from politicos.filters import DeputadoFilter
from politicos.models import Deputado
from politicos.serializers import DeputadoSerializer


class DeputadoListView(generics.ListAPIView):
    serializer_class = DeputadoSerializer
    filterset_class = DeputadoFilter
    queryset = Deputado.objects.all().select_related('partido', 'uf')
