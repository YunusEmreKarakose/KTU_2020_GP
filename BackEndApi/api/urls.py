from django.urls import path
from .views import DetectFacesViewSet
urlpatterns = [
    path('detectFaces/', DetectFacesViewSet.as_view()),
]