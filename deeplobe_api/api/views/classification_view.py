from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from ..serializers import (
    FileAssetSerializer
)

class ClassificationImageUpload(APIView):

    def post(self, request):
        myDict = dict(request.data)
        print(myDict)
        try:
            dict_data = [
                {"name": str(i), "asset": myDict["asset[]"][index]}
                for index, i in enumerate(myDict["asset[]"])
            ]
            
        except Exception as e:
            return Response(
                {"Error": "Payload error" + str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = FileAssetSerializer(data=dict_data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)