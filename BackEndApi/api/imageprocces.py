#face recog and image proccess
import face_recognition
from PIL import Image,ImageDraw
import random

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
        #return proccesed and saved image path in server
        return './uploadedImages/proccesed/proccesed'+splittedPath[4]
    #detectSpecificFace
    def detectSpecificFace(imagePath,targetIFPath,targetName):
        #imagename splittedPath[4]
        splittedPath=imagePath.split("/")
        #target image
        targetImage=face_recognition.load_image_file(targetIFPath)
        targetFaceEncode=face_recognition.face_encodings(targetImage)[0]
        knownFaceEncodings=[
            targetFaceEncode
        ]
        #picture with face inside
        image=face_recognition.load_image_file(imagePath)
        #find faces in image
        faceLocations=face_recognition.face_locations(image)
        faceEncodings=face_recognition.face_encodings(image,faceLocations)
        #convert to PIL format
        pilImage=Image.fromarray(image)
        #draw
        draw=ImageDraw.Draw(pilImage)
        #loop through faces in image
        for (top,right,bottom,left),faceEncoding in zip(faceLocations,faceEncodings):
            matches=face_recognition.compare_faces(knownFaceEncodings,faceEncoding)
            
            #if match
            if True in matches:
                firstMatchIndex=matches.index(True)
                name=targetName            
                #draw box
                draw.rectangle(((left,top),(right,bottom)),outline=(0,0,0))
                #draw label
                textWdith,textHeight=draw.textsize(name)
                draw.rectangle(((left,bottom-textHeight-10),(right,bottom)),fill=(0,0,0),outline=(0,0,0))
                draw.text((left+6,bottom-textHeight-5),name,fill=(255,255,255,255))
        del draw        
        pilImage.save('./uploadedImages/proccesed/proccesed'+splittedPath[4])
        #return proccesed and saved image path in server
        return './uploadedImages/proccesed/proccesed'+splittedPath[4]
    
    #corrupt image with factor
    def corrupt(image,coordinates,factor):
        #crop image with top-left and right-bottom coordinates
        pieces=[]
        xDimension=coordinates['bottomRightX']-coordinates['topLeftX']
        yDimension=coordinates['bottomRightY']-coordinates['topLeftY']
        for i in range(int(xDimension/factor)):
            for j in range(int(yDimension/factor)):
                ctopleftx=coordinates['topLeftX']+i*factor
                ctoplefty=coordinates['topLeftY']+j*factor
                cbotrightx=coordinates['topLeftX']+i*factor+factor
                cbotrighty=coordinates['topLeftY']+i*factor+factor
                #print("crop coordinates topleft i::"+str(i*factor)+" j::"+str(j*factor)+ "  toprighti::"+str(i*factor+2)+" j::"+str(j*factor+2) )
                #print("cropped "+str(ctopleftx)+"  "+str(ctoplefty)+"  "+str(cbotrightx)+"  "+str(cbotrighty))
                pieces.append(image.crop((ctopleftx,ctoplefty,cbotrightx,cbotrighty)))
        
        #paste cropped pieces random coordinates and save
        list=[]#picked random index list
        for i in range(int(xDimension/factor)):
            for j in range(int(yDimension/factor)):
                ctopleftx=coordinates['topLeftX']+i*factor
                ctoplefty=coordinates['topLeftY']+j*factor
                cbotrightx=coordinates['topLeftX']+i*factor+factor
                cbotrighty=coordinates['topLeftY']+i*factor+factor
                #random image pick from pieces
                r=random.randint(0,len(pieces)-1)
                while r not in list:
                    list.append(r)        
                    r=random.randint(0,len(pieces)-1)
                #print("piece "+str(r)+" paste to "+str(ctopleftx)+"  "+str(ctoplefty)+"  "+str(cbotrightx)+"  "+str(cbotrighty))            
                image.paste(pieces[r],(ctopleftx,ctoplefty))
        return image
    #detect face and corrupt
    def detectSFaceAndCorrupt(imagePath,targetIFPath,factor=16):
        #imagename splittedPath[4]
        splittedPath=imagePath.split("/")        
        #target image
        targetImage=face_recognition.load_image_file(targetIFPath)
        targetFaceEncode=face_recognition.face_encodings(targetImage)[0]
        knownFaceEncodings=[
            targetFaceEncode
        ]
        #picture with face inside
        image=face_recognition.load_image_file(imagePath)
        #find faces in picture
        faceLocations=face_recognition.face_locations(image)
        faceEncodings=face_recognition.face_encodings(image,faceLocations)

        #convert to PIL format
        pilImage=Image.fromarray(image)

        #loop through faces in image
        for (top,right,bottom,left),faceEncoding in zip(faceLocations,faceEncodings):
            matches=face_recognition.compare_faces(knownFaceEncodings,faceEncoding)
            
            #if match
            if True in matches:
                #call corrupt
                coordinates={
                    'topLeftX':left,
                    'topLeftY':top,
                    'bottomRightX':right,
                    'bottomRightY':bottom
                }
                pilImage=ImageProccess.corrupt(pilImage,coordinates,factor)
        pilImage.save('./uploadedImages/proccesed/proccesed'+splittedPath[4])
        #return proccesed and saved image path in server
        return './uploadedImages/proccesed/proccesed'+splittedPath[4]
                