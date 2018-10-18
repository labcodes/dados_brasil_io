from django_filters import rest_framework as filters

from politicos.models import Deputado


class DeputadoFilter(filters.FilterSet):
    nome = filters.CharFilter(field_name='nome', lookup_expr='icontains')
    exibir_gasto_mensal = filters.BooleanFilter(method='filter_exibir_gasto_mensal')

    class Meta:
        model = Deputado
        fields = [
            'nome', 'partido', 'uf', 'id_legislatura',
        ]

    def filter_exibir_gasto_mensal(self, queryset, name, value):
        if value and not {'gastos_mes', 'gastos_ano'} & set(self.data.keys()):
            queryset = queryset.annotate_gasto_mensal_por_deputado()
        return queryset
