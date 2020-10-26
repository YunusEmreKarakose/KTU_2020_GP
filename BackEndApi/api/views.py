#django rest framework imports
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
#face recog and image proccess
from api.imageprocces import ImageProccess
#models
from .models import DetectFacesModel
from .serializers import DetectFacesSerializer

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