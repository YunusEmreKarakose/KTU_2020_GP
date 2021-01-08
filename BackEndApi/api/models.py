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
#detect specific face and corrupt
class DetectSFaceAndCorruptModel(models.Model):
    corruptFactor=models.IntegerField(default=8,null=True)
    image=models.ImageField(upload_to='images',null=True,blank=True)
    targetImage=models.ImageField(upload_to='images',null=True,blank=True)
    def __str__(self):
        return self.targetName
#myfaceDetection
class MyFaceDetection(models.Model):
    image=models.ImageField(upload_to='images',null=True,blank=True)
    def __str__(self):
        return self.image
