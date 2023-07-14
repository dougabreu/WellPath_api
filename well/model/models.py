from django.db import models


class Wells(models.Model):

    #id_well = models.CharField(max_length=255)  # nome do arquivo + numero +tipo poço + trajetoria
    #title = models.CharField(max_length=255)  # nome arquivo + usuario
    #author = models.CharField(max_length=255) # usuario solicitou otm

    # well vertical
    cabeca_poco = models.CharField(max_length=255)
    kop = models.CharField(max_length=255)
    eob = models.CharField(max_length=255)
    inicio_objetivo = models.CharField(max_length=255)
    fim_objetivo = models.CharField(max_length=255)
    angulo = models.CharField(max_length=255)
    direcao_objetivo = models.CharField(max_length=255)
    afastamento_objetivo = models.CharField(max_length=255)
    profundidade_vertical = models.CharField(max_length=255)
    trecho_cabeca_kop = models.CharField(max_length=255)
    trecho_arco_buildup = models.CharField(max_length=255)
    trecho_slant = models.CharField(max_length=255)
    trecho_canhoneado = models.CharField(max_length=255)
    comprimento_total = models.CharField(max_length=255)

    # well tipo 2
    # drop_off_xyz = models.CharField(max_length=255)
    # trecho_reto = models.CharField(max_length=255)
    # trecho_drop_off = models.CharField(max_length=255)
    # trecho_verticalizacao = models.CharField(max_length=255)

