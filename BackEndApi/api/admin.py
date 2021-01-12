from django.contrib import admin
#models
from .models import DetectFacesModel,DetectSpecificFacesModel,DetectSFaceAndCorruptModel,MyFaceDetection

# Register your models here.
admin.site.register(DetectFacesModel)
admin.site.register(DetectSpecificFacesModel)
admin.site.register(DetectSFaceAndCorruptModel)
admin.site.register(MyFaceDetection)