#django rest framework imports
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse,FileResponse
import base64
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
#myfacedetection
from .models import MyFaceDetection
from .serializers import MyFaceDetectionSerializer

# Create your views here.
class DetectFacesViewSet(APIView):
    queryset=DetectFacesModel.objects.all()
    parser_classes=(MultiPartParser,FormParser)

    #post
    def post(self,request,*args,**kwargs):
        df_serializers=DetectFacesSerializer(data=request.data)
        if df_serializers.is_valid():
            df_serializers.save()
            #find faces            
            faces=ImageProccess.detectFaces('./'+df_serializers.data['image'])
            #draw rectangels
            proccesedImgPath=ImageProccess.drawRectangelsDlib('./'+df_serializers.data['image'],faces)
            #return proccesed img as response
            pImg=open(proccesedImgPath,'rb')            
            #file response for react
            b64str=base64.b64encode(pImg.read())
            return HttpResponse(b64str)
            #return FileResponse(pImg)
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
            #find matches
            matches=ImageProccess.faceRecog(imagePath,targetIFPath)
            #draw rectangle
            proccesedImgPath=ImageProccess.drawRectangelsDlib(imagePath,matches)
            #return proccesed img as response
            pImg=open(proccesedImgPath,'rb')
            #file response for react
            b64str=base64.b64encode(pImg.read())
            return HttpResponse(b64str)
            #return FileResponse(pImg)
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
            #find matches
            matches=ImageProccess.faceRecog(imagePath,targetIFPath)
            #matche coordinate
            coordinates={'topLeftY':matches[0].top(),'bottomRightY':matches[0].bottom(),'topLeftX':matches[0].left(),'bottomRightX':matches[0].right()}
            #corrupt
            proccesedImgPath=ImageProccess.corrupt(imagePath,coordinates,corruptFactor)
            #return proccesed img as response
            pImg=open(proccesedImgPath,'rb')
            #file response for react
            b64str=base64.b64encode(pImg.read())
            return HttpResponse(b64str)
            #for postman
            #return FileResponse(pImg)     
        else:
            return Response(dsf_serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    

#myFaceDetection
class MFDViewSet(APIView):
    queryset=MyFaceDetection.objects.all()
    parser_classes=(MultiPartParser,FormParser)
    #post
    def post(self,request,*args,**kwargs):
        mfd_serializer=MyFaceDetectionSerializer(data=request.data)
        if mfd_serializer.is_valid():
            mfd_serializer.save()
            #get face location
            faceLocations=ImageProccess.myFaceDetection('./'+mfd_serializer.data['image'])
            #draw
            proccesedImgPath=ImageProccess.drawRectangels('./'+mfd_serializer.data['image'],faceLocations)
            #return proccesed img as response
            pImg=open(proccesedImgPath,'rb')            
            #file response for react
            b64str=base64.b64encode(pImg.read())
            return HttpResponse(b64str)        
        else:
            return Response(mfd_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            