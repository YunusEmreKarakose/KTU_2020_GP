#django rest framework imports
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse,FileResponse
#face recog and image proccess
from api.imageprocces import ImageProccess
#models
#detect faces
from .models import DetectFacesModel
from .serializers import DetectFacesSerializer
#dtect specific faces
from .models import DetectSpecificFacesModel
from .serializers import DetectSpecificFacesSerializer
#detect specific faces and corrupt
from .models import DetectSFaceAndCorruptModel
from .serializers import DetectSFaceAndCorruptSerializer
# Create your views here.
class DetectFacesViewSet(APIView):
    queryset=DetectFacesModel.objects.all()
    parser_classes=(MultiPartParser,FormParser)

    #post
    def post(self,request,*args,**kwargs):
        df_serializers=DetectFacesSerializer(data=request.data)
        if df_serializers.is_valid():
            df_serializers.save()            
            proccesedImgPath=ImageProccess.detectFaces('./'+df_serializers.data['image'])
            #return proccesed img as response
            pImg=open(proccesedImgPath,'rb')
            return FileResponse(pImg)
            #return Response(df_serializers.data,status=status.HTTP_201_CREATED)
        else:
            return Response(df_serializers.errors,status=status.HTTP_400_BAD_REQUEST)

#detect specific face 
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
            proccesedImgPath=ImageProccess.detectSpecificFace(imagePath,targetIFPath,targetName)
            #return proccesed img as response
            pImg=open(proccesedImgPath,'rb')
            return FileResponse(pImg)
            #return Response(dsf_serializers.data,status=status.HTTP_201_CREATED)
        else:
            return Response(dsf_serializers.errors,status=status.HTTP_400_BAD_REQUEST)
#detect specific face and corrupt
class DSFACViewSet(APIView):
    queryset=DetectSpecificFacesModel.objects.all()
    parser_classes=(MultiPartParser,FormParser)
    #post
    def post(self,request,*args,**kwargs):
        dsf_serializers=DetectSFaceAndCorruptSerializer(data=request.data)
        if dsf_serializers.is_valid():
            dsf_serializers.save()
            imagePath='./'+dsf_serializers.data['image']
            targetIFPath='./'+dsf_serializers.data['targetImage']
            corruptFactor=dsf_serializers.data['corruptFactor']
            proccesedImgPath=ImageProccess.detectSFaceAndCorrupt(imagePath,targetIFPath,corruptFactor)
            #return proccesed img as response
            pImg=open(proccesedImgPath,'rb')
            return FileResponse(pImg)
            #return Response(dsf_serializers.data,status=status.HTTP_201_CREATED)
        else:
            return Response(dsf_serializers.errors,status=status.HTTP_400_BAD_REQUEST)