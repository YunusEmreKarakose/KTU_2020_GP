from rest_framework import serializers
from .models import DetectFacesModel

class DetectFacesSerializer(serializers.ModelSerializer):
    class Meta():
        model=DetectFacesModel
        fields=['title','image']