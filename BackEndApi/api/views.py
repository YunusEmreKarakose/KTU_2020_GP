#django rest framework imports
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
#face recog and image proccess
from api.imageprocces import ImageProccess
#models
from .models import DetectFacesModel,DetectSpecificFacesModel
from .serializers import DetectFacesSerializer,DetectSpecificFacesSerializer

# Create your views here.
class DetectFacesViewSet(APIView):
    queryset=DetectFacesModel.objects.all()
    parser_classes=(MultiPartParser,FormParser)

    #post
    def post(self,request,*args,**kwargs):
        df_serializers=DetectFacesSerializer(data=request.data)
        if df_serializers.is_valid():
            df_serializers.save()            
            ImageProccess.detectFaces('./'+df_serializers.data['image'])
            return Response(df_serializers.data,status=status.HTTP_201_CREATED)
        else:
            return Response(df_serializers.errors,status=status.HTTP_400_BAD_REQUEST)

#detect specific face detect
class DSFViewSet(APIView):
    queryset=DetectSpecificFacesModel.objects.all()
    parser_classes=(MultiPartParser,FormParser)

    #post
    def post(self,request,*args,**kwargs):
        dsf_serializers=DetectSpecificFacesSerializer(data=request.data)
        if dsf_serializers.is_valid():
            dsf_serializers.save()
            imagePath='./'+dsf_serializers.data['image']
            targetIFPath='./'+dsf_serializers.data['targetImage']
            targetName=dsf_serializers.data['targetName']
            ImageProccess.detectSpecificFace(imagePath,targetIFPath,targetName)
            return Response(dsf_serializers.data,status=status.HTTP_201_CREATED)
        else:
            return Response(dsf_serializers.errors,status=status.HTTP_400_BAD_REQUEST)