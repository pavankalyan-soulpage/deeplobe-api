import PIL
import os
from PIL import Image         
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

class ClassificationImageUpload(APIView):

    def post(self, request, category_name):
        
        for x in request.FILES.getlist("asset[]"):
            # creating a image object (main image) 
            im1 = Image.open(x) 
            
            # save a image using extension
            if not os.path.isdir(os.path.join("deeplobe_ai", "Datasets", "classification", category_name)):
                    os.makedirs(os.path.join("deeplobe_ai", "Datasets", "classification", category_name))
            im1 = im1.save(f"deeplobe_ai/Datasets/classification/{category_name}/{x}")
    

        return Response({"msg": "Uploded successfully"}, status=status.HTTP_200_OK)
