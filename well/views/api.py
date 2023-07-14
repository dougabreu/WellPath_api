from rest_framework.decorators import api_view
from rest_framework.response import Response
from well.model.TrajectoryModel import TrajectoryServiceManager
from WellPath_api.serializers import WellSerializer
from ..model.models import Wells

from tkinter import Tk
from tkinter import filedialog

from ..utils.generalUtils import deserializer


@api_view()
def well_api_list(request):

    well_api_save()

    well = Wells.objects.all()
    serializer = WellSerializer(instance=well, many=True, context={'request': request})
    return Response(serializer.data)


def well_api_save():

    #Tk().withdraw()

    #input_data = filedialog.askopenfilename(
    #    title='Buscar arquivo de poço',
    #    initialdir='D:\\Well_Path\\Documents\\input'
    #)

    input_data = 'D:\\Well_Path\\Documents\\input\\tipo1_test.json'
    well_info = deserializer(input_data)

    for well in well_info:
        data_well = TrajectoryServiceManager(well_info[well]).check_target_trajectory()

        serializer = WellSerializer(data=data_well)
        serializer.is_valid(raise_exception=True)
        serializer.save()

