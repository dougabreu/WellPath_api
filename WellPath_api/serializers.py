from rest_framework import serializers
from well.model import models


class WellSerializer(serializers.Serializer):
    class Meta:
        model = models.Wells
        fields = ['cabeca_poco', 'kop', 'eob', 'objetivo', 'fim_objetivo', 'angulo', 'direcao_objetivo',
                   'afastamento_objetivo', 'profundidade_vertical', 'trecho_cabeca_kop', 'trecho_arco_buildup',
                   'trecho_slant', 'trecho_canhoneado', 'comprimento_total']

        # well vertical
        cabeca_poco = serializers.FloatField()
        inicio_objetivo = serializers.FloatField()
        fim_objetivo = serializers.FloatField()

        # well tipo 1
        #cabeca_poco = serializers.FloatField()
        kop = serializers.FloatField()
        eob = serializers.FloatField()
        objetivo = serializers.FloatField()
        #fim_objetivo = serializers.FloatField()
        angulo = serializers.FloatField()
        direcao_objetivo = serializers.FloatField()
        afastamento_objetivo = serializers.FloatField()
        profundidade_vertical = serializers.FloatField()
        trecho_cabeca_kop = serializers.FloatField()
        trecho_arco_buildup = serializers.FloatField()
        trecho_slant = serializers.FloatField()
        trecho_canhoneado = serializers.FloatField()
        comprimento_total = serializers.FloatField()

        # well tipo 2
        #cabeca_poco = serializers.FloatField()
        first_kop = serializers.FloatField()
        #eob = serializers.FloatField()
        drop_off_xyz = serializers.FloatField()
        trecho_reto = serializers.FloatField()
        #objetivo = serializers.FloatField()
        #fim_objetivo = serializers.FloatField()
        #angulo = serializers.FloatField()
        #direcao_objetivo = serializers.FloatField()
        #afastamento_objetivo = serializers.FloatField()
        #profundidade_vertical = serializers.FloatField()
        #trecho_cabeca_kop = serializers.FloatField()
        #trecho_arco_buildup = serializers.FloatField()
        #trecho_slant = serializers.FloatField()
        trecho_drop_off = serializers.FloatField()
        trecho_verticalizacao = serializers.FloatField()
        #trecho_canhoneado = serializers.FloatField()
        #comprimento_total = serializers.FloatField()
