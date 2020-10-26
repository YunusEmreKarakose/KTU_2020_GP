from django.db import models

# Create your models here.
#face detection model
class DetectFacesModel(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to='images',null=True,blank=True)

    def __str__(self):
        return self.title
#detect specific face
class DetectSpecificFacesModel(models.Model):
    targetName=models.CharField(max_length=100)
    image=models.ImageField(upload_to='images',null=True,blank=True)
    targetImage=models.ImageField(upload_to='images',null=True,blank=True)
    def __str__(self):
        return self.targetName
