from datetime import date
from rest_framework import generics, serializers
from rest_framework.response import Response

from politicos.models import Deputado


class DeputadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deputado
        fields = ['id', 'partido', 'uf', 'id_legislatura', 'carteira_parlamentar', 'gastos']
        depth = 2


class DeputadoListView(generics.ListAPIView):
    queryset = Deputado.objects.all().select_related('partido', 'uf')
    serializer_class = DeputadoSerializer

    def list(self, request):
        today = date.today()
        queryset = self.get_queryset()
        mes = request.query_params.get('mes', today.month)
        ano = request.query_params.get('ano', today.year)
        queryset = queryset.prefetch_gastos_mes(mes=mes, ano=ano)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

