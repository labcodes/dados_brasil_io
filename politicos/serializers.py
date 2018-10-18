from rest_framework import serializers

from politicos.models import Deputado, GastoCotaParlamentar


class GastoCotaParlamentarSerializer(serializers.ModelSerializer):
    class Meta:
        model = GastoCotaParlamentar
        fields = [
            'id',
            'data_emissao',
            'ano',
            'especificacao_subcota',
            'mes',
            'ressarcimento',
            'cpf',
            'descricao',
            'descricao_especificacao',
            'fornecedor',
            'valor_documento',
            'valor_glosa',
            'valor_liquido',
            'valor_restituicao',
            'empresa',
        ]
        depth = 1


class DeputadoSerializer(serializers.ModelSerializer):
    gastos_mensais = serializers.SerializerMethodField()
    gastos = GastoCotaParlamentarSerializer(many=True)

    class Meta:
        model = Deputado
        fields = [
            'id', 'nome', 'partido', 'uf', 'id_legislatura',
            'gastos', 'gastos_mensais',
        ]
        depth = 2

    def get_gastos_mensais(self, obj):
        return {
            key: value for key, value in obj.__dict__.items()
            if key.startswith('gastos_')
        }
