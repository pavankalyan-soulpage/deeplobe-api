import PIL
import os
import json
from PIL import Image         
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

class TaggingImageUpload(APIView):

    def post(self, request):
        
        for x in request.FILES.getlist("asset[]"):

            filename, file_extension = os.path.splitext(x.name)

            if file_extension == ".json":
                if not os.path.isdir(os.path.join("deeplobe_ai", "Datasets", "Detection", "annotations")):
                    os.makedirs(os.path.join("deeplobe_ai", "Datasets", "Detection", "annotations"))

                with open(
                    os.path.join("deeplobe_ai", "Datasets", "Detection", "annotations", "coco_instances.json"),
                    "w",
                    encoding="utf-8",
                ) as f:
                    json.dump(json.loads(x.read()), f, ensure_ascii=False, indent=4)
            else:
                im1 = Image.open(x) 
                
                # save a image using extension
                if not os.path.isdir(os.path.join("deeplobe_ai", "Datasets", "Detection", "images")):
                        os.makedirs(os.path.join("deeplobe_ai", "Datasets", "Detection", "images"))
                im1 = im1.save(f"deeplobe_ai/Datasets/Detection/images/{x}")
    

        return Response({"msg": "Uploded successfully"}, status=status.HTTP_200_OK)
