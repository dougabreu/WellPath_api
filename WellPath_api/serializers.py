from rest_framework import serializers
from well.model.models import Wells


class WellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wells
        fields = ['tipo_trajetoria', 'cabeca_poco', 'kop', 'second_kop', 'eob', 'drop_off_xyz', 'trecho_reto', 'inicio_objetivo',
                  'fim_objetivo', 'angulo', 'angulo_first_kop', 'angulo_second_kop', 'direcao_objetivo',
                  'afastamento_objetivo', 'trecho_cabeca_kop', 'trecho_arco_buildup', 'trecho_slant', 'trecho_drop_off',
                  'trecho_verticalizacao', 'trecho_canhoneado',  'profundidade_vertical', 'comprimento_total']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {k: v for k, v in data.items() if v is not None}
