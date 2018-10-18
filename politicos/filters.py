from django_filters import rest_framework as filters

from politicos.models import Deputado


class DeputadoFilter(filters.FilterSet):
    nome = filters.CharFilter(field_name='nome', lookup_expr='icontains')
    exibir_gasto_mensal = filters.BooleanFilter(method='filter_exibir_gasto_mensal')
    gastos_mes = filters.NumberFilter(method='add_prefetch_gastos')
    gastos_ano = filters.NumberFilter(method='add_prefetch_gastos')

    class Meta:
        model = Deputado
        fields = [
            'nome', 'partido', 'uf', 'id_legislatura',
        ]

    def filter_exibir_gasto_mensal(self, queryset, name, value):
        if value and not {'gastos_mes', 'gastos_ano'} & set(self.data.keys()):
            queryset = queryset.annotate_gasto_mensal_por_deputado()
        return queryset

    def add_prefetch_gastos(self, queryset, name, value):
        filtros = self.data.dict()
        mes = filtros.get('gastos_mes')
        ano = filtros.get('gastos_ano')
        if not hasattr(self, '_prefetch_added') and mes and ano:
            queryset = queryset.prefetch_gastos(mes=mes, ano=ano)
            self._prefetch_added = True
        return queryset
