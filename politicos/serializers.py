from rest_framework import serializers

from politicos.models import Deputado, GastoCotaParlamentar


class GastoCotaParlamentarSerializer(serializers.ModelSerializer):
    class Meta:
        model = GastoCotaParlamentar
        fields = '__all__'


class DeputadoSerializer(serializers.ModelSerializer):
    gastos_mensais = serializers.SerializerMethodField()

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
