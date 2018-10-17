from django_filters import rest_framework as filters

from politicos.models import Deputado


class DeputadoFilter(filters.FilterSet):
    nome = filters.CharFilter(field_name='nome', lookup_expr='icontains')

    class Meta:
        model = Deputado
        fields = [
            'nome', 'partido', 'uf', 'id_legislatura',
        ]
