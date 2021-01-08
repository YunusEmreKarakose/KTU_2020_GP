from django.urls import path
from .views import DetectFacesViewSet,DSFViewSet,DSFACViewSet,MFDViewSet
urlpatterns = [
    path('detectFaces/', DetectFacesViewSet.as_view()),
    path('detectSpecificFaces/', DSFViewSet.as_view()),
    path('detectSFaceAndCorrupt/', DSFACViewSet.as_view()),
    path('myFaceDetection/', MFDViewSet.as_view()),
]