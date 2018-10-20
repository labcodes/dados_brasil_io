from rest_framework import generics, serializers
from rest_framework.response import Response

from empresas.models import Empresa, Sociedade


class EmpresaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Empresa
        fields = ['cnpj', 'nome', 'sociedades']
        depth = 10


class EmpresaDetailView(generics.RetrieveAPIView):
    serializer_class = EmpresaSerializer
    queryset = Empresa.objects.all()

