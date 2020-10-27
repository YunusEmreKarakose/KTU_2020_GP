from django.contrib import admin
#models
from .models import DetectFacesModel,DetectSpecificFacesModel,DetectSFaceAndCorruptModel

# Register your models here.
admin.site.register(DetectFacesModel)
admin.site.register(DetectSpecificFacesModel)
admin.site.register(DetectSFaceAndCorruptModel)