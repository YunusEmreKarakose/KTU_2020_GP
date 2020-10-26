#face recog and image proccess
import face_recognition
from PIL import Image,ImageDraw

class ImageProccess():
    def __init__(self):
        self.image=image
    
    def detectFaces(imagePath):
        #imagename splittedPath[4]
        splittedPath=imagePath.split("/")
        #image
        image=face_recognition.load_image_file(imagePath)
        #find faces in image
        faceLocations=face_recognition.face_locations(image)    
        #convert to PIL format
        pilImage=Image.fromarray(image)
        #draw
        draw=ImageDraw.Draw(pilImage)#loop through faces in image
        for top,right,bottom,left in faceLocations:        
            name="Unknown"        
            #draw box
            draw.rectangle(((left,top),(right,bottom)),outline=(0,0,0))
            #draw label
            textWdith,textHeight=draw.textsize(name)
            draw.rectangle(((left,bottom-textHeight-10),(right,bottom)),fill=(0,0,0),outline=(0,0,0))
            draw.text((left+6,bottom-textHeight-5),name,fill=(255,255,255,255))
        #delete draw instance
        del draw
        #display
        pilImage.save('./uploadedImages/proccesed/proccesed'+splittedPath[4])