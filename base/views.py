import json

import pandas as pd
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from base.tasks import celery_function

from .models import File
from .serializers import FileSerializer


class FileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Files to be viewed or edited.
    """

    parser_classes = (MultiPartParser,)
    queryset = File.objects.all()
    serializer_class = FileSerializer


@api_view(['GET'])
def process_file(request, id):
    try:
        file = File.objects.get(id=id)
        df = pd.read_excel(file.file, na_values=['-']).convert_dtypes().fillna(0)
        task = celery_function.delay(json.dumps(df.to_dict()))
        return Response({'task': task.id}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
