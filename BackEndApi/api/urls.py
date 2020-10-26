from django.urls import path
from .views import DetectFacesViewSet,DSFViewSet
urlpatterns = [
    path('detectFaces/', DetectFacesViewSet.as_view()),
    path('detectSpecificFaces/', DSFViewSet.as_view()),
]