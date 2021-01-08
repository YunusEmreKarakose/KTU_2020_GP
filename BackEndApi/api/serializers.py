from rest_framework import serializers
from .models import DetectFacesModel,DetectSpecificFacesModel,DetectSFaceAndCorruptModel,MyFaceDetection

class DetectFacesSerializer(serializers.ModelSerializer):
    class Meta():
        model=DetectFacesModel
        fields=['title','image']

class DetectSpecificFacesSerializer(serializers.ModelSerializer):
    class Meta():
        model=DetectSpecificFacesModel
        fields=['targetName','image','targetImage']
class DetectSFaceAndCorruptSerializer(serializers.ModelSerializer):
    class Meta():
        model=DetectSFaceAndCorruptModel
        fields=['corruptFactor','image','targetImage']
class MyFaceDetectionSerializer(serializers.ModelSerializer):
    class Meta():
        model=MyFaceDetection
        fields=['image']