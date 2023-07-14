from django.db import models


class Wells(models.Model):

    #id_well = models.CharField(max_length=255)  # nome do arquivo + numero +tipo poço + trajetoria
    #title = models.CharField(max_length=255)  # nome arquivo + usuario
    #author = models.CharField(max_length=255) # usuario solicitou otm

    # wells
    cabeca_poco = models.CharField(max_length=255)
    kop = models.CharField(max_length=255, null=True)
    second_kop = models.CharField(max_length=255, null=True)
    eob = models.CharField(max_length=255, null=True)
    drop_off_xyz = models.CharField(max_length=255, null=True)
    trecho_reto = models.CharField(max_length=255, null=True)
    inicio_objetivo = models.CharField(max_length=255)
    fim_objetivo = models.CharField(max_length=255)

    angulo = models.CharField(max_length=255, null=True)
    angulo_first_kop = models.CharField(max_length=255, null=True)
    angulo_second_kop = models.CharField(max_length=255, null=True)

    direcao_objetivo = models.CharField(max_length=255, null=True)
    afastamento_objetivo = models.CharField(max_length=255, null=True)

    trecho_cabeca_kop = models.CharField(max_length=255, null=True)
    trecho_arco_buildup = models.CharField(max_length=255, null=True)
    trecho_slant = models.CharField(max_length=255, null=True)
    trecho_drop_off = models.CharField(max_length=255, null=True)
    trecho_verticalizacao = models.CharField(max_length=255, null=True)
    trecho_canhoneado = models.CharField(max_length=255, null=True)
    profundidade_vertical = models.CharField(max_length=255, null=True)
    comprimento_total = models.CharField(max_length=255, null=True)








