from rest_framework.decorators import api_view
from rest_framework.response import Response
from well.model.TrajectoryModel import TrajectoryServiceManager
from WellPath_api.serializers import serializers
from ..model.models import Wells

from tkinter import Tk
from tkinter import filedialog


@api_view()
def well_api_list(request):
    Tk().withdraw()

    input_data = filedialog.askopenfilename(
        title='Buscar arquivo de poço',
        initialdir='D:\\Well_Path\\Documents\\input'
    )

    save_data_well = TrajectoryServiceManager(input_data).check_target_trajectory()

    well = Wells.objects.get()
    serializer = serializers.ModelSerializer(instance=well)
    return Response(serializer)
