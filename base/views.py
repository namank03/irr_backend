import json

import numpy_financial as npf
import pandas as pd
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

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
    file = File.objects.get(id=id)

    df = pd.read_excel(file.file, na_values=['-']).convert_dtypes().fillna(0)
    prn_df = df.filter(like='PRN')
    x3 = df['X3']
    x6 = df['X6']
    x5 = df['X5']
    y1 = x3 * x6
    prn_df = pd.concat([(x3 - y1 + x5) * -1, prn_df], axis=1).convert_dtypes()

    irr_df = pd.concat([df['X1'], prn_df.apply(npf.irr, axis=1) * 100], axis=1).rename(
        columns={0: "IRR"}
    )

    res = json.dumps(irr_df.to_dict('records'))
    return Response(res)
