from rest_framework import serializers
from .models import DetectFacesModel,DetectSpecificFacesModel

class DetectFacesSerializer(serializers.ModelSerializer):
    class Meta():
        model=DetectFacesModel
        fields=['title','image']

class DetectSpecificFacesSerializer(serializers.ModelSerializer):
    class Meta():
        model=DetectSpecificFacesModel
        fields=['targetName','image','targetImage']