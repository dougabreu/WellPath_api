from django.db import models


class Wells(models.Model):

    id_well = models.CharField(max_length=255)  # nome do arquivo + numero +tipo poço + trajetoria
    title = models.CharField(max_length=255)  # nome arquivo + usuario
    author = models.CharField(max_length=255) # usuario solicitou otm

    # well vertical
    cabeca_poco = models.FloatField()
    inicio_objetivo = models.FloatField()
    fim_objetivo = models.FloatField()

    # well tipo 1
    # cabeca_poco = serializers.FloatField()
    kop = models.FloatField()
    eob = models.FloatField()
    objetivo = models.FloatField()
    # fim_objetivo = serializers.FloatField()
    angulo = models.FloatField()
    direcao_objetivo = models.FloatField()
    afastamento_objetivo = models.FloatField()
    profundidade_vertical = models.FloatField()
    trecho_cabeca_kop = models.FloatField()
    trecho_arco_buildup = models.FloatField()
    trecho_slant = models.FloatField()
    trecho_canhoneado = models.FloatField()
    comprimento_total = models.FloatField()

    # well tipo 2
    # cabeca_poco = serializers.FloatField()
    first_kop = models.FloatField()
    # eob = serializers.FloatField()
    drop_off_xyz = models.FloatField()
    trecho_reto = models.FloatField()
    # objetivo = serializers.FloatField()
    # fim_objetivo = serializers.FloatField()
    # angulo = serializers.FloatField()
    # direcao_objetivo = serializers.FloatField()
    # afastamento_objetivo = serializers.FloatField()
    # profundidade_vertical = serializers.FloatField()
    # trecho_cabeca_kop = serializers.FloatField()
    # trecho_arco_buildup = serializers.FloatField()
    # trecho_slant = serializers.FloatField()
    trecho_drop_off = models.FloatField()
    trecho_verticalizacao = models.FloatField()
    # trecho_canhoneado = serializers.FloatField()
    # comprimento_total = serializers.FloatField()

