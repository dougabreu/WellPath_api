from rest_framework import serializers
from well.model.models import Wells


class WellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wells
        fields = ['cabeca_poco', 'inicio_objetivo', 'fim_objetivo', 'kop', 'eob', 'angulo', 'direcao_objetivo',
                  'afastamento_objetivo', 'profundidade_vertical', 'trecho_cabeca_kop', 'trecho_arco_buildup',
                  'trecho_slant', 'trecho_canhoneado', 'comprimento_total']

