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

    #myFaceDetection
    def myFaceDetection(imagePath):
        #RGB
        imageRGB=Image.open(imagePath)
        rgbPixels=imageRGB.load()
        width,height=imageRGB.size
        #YCbCr
        imageYCBCR=Image.open(imagePath).convert('YCbCr')
        ycbcrPixels=imageYCBCR.load()
        #factor
        factor=2
        if width>1000 and height>1000:
            factor=4
        if width>2000 and height>2000:
            factor=8
        if width>3000:
            factor=16
        #parse image factorxfactor pieces
        widthRange=int(width/factor)
        heightRange=int(height/factor)
        #possible face piece
        pArr=[]
        for i in range(widthRange*heightRange):
            pArr.append({"isSkin":False,"isUsed":False,"avrjR":0,"avrjG":0,"avrjB":0,"avrjY":0,"avrjCb":0,"avrjCr":0})
        #calculate avarage RGB and YCbCr of pieces
        for i in range(heightRange):
            for j in range(widthRange):
                #print("seach for piece"+str(j+(i*widthRange)))
                #print("left("+str(factor*j)+") upper("+str(factor*i)+") right("+str(factor*j+factor)+") lower("+str(factor*i+factor)+")")
                #rgb piece
                rgbPiece=imageRGB.crop(((factor*j),(factor*i),(factor*j+factor),(factor*i+factor)))
                rgbPiecePixels=rgbPiece.load()
                #YCbCr piece
                ycbcrPiece=imageYCBCR.crop(((factor*j),(factor*i),(factor*j+factor),(factor*i+factor)))
                ycbcrPiecePixels=ycbcrPiece.load()

                #find piece average rgb and YCbCr
                dictTmp=pArr[j+(i*widthRange)]
                for m in range(factor):
                    for n in range(factor):
                        #rgb
                        r,g,b=rgbPiecePixels[m,n]
                        dictTmp["avrjR"]+=r
                        dictTmp["avrjG"]+=g
                        dictTmp["avrjB"]+=b
                        #ycbcr
                        y,cb,cr=ycbcrPiecePixels[m,n]
                        dictTmp["avrjY"]+=y
                        dictTmp["avrjCb"]+=cb
                        dictTmp["avrjCr"]+=cr
                #set piece average rgb values
                dictTmp["avrjR"]=dictTmp["avrjR"]/(factor*factor)
                dictTmp["avrjG"]=dictTmp["avrjG"]/(factor*factor)
                dictTmp["avrjB"]=dictTmp["avrjB"]/(factor*factor)
                #ycbcr
                dictTmp["avrjY"]=dictTmp["avrjY"]/(factor*factor)
                dictTmp["avrjCb"]=dictTmp["avrjCb"]/(factor*factor)
                dictTmp["avrjCr"]=dictTmp["avrjCr"]/(factor*factor)

        #find possible skin piece
        for i in range(len(pArr)):
            dictTmp=pArr[i]
            #R > 95 and G > 40 and B > 20 and 
            condition1=False
            if dictTmp["avrjR"]>95 and dictTmp["avrjG"]>40 and dictTmp["avrjB"]>20 :
                condition1=True
            #R > G and R > B and | R - G | > 15 and
            condition2=False
            if dictTmp["avrjR"]>dictTmp["avrjG"] and dictTmp["avrjR"]>dictTmp["avrjB"] and abs(dictTmp["avrjR"]-dictTmp["avrjG"])>15:
                condition2=True
            #Cr > 135 and Cb > 85 and Y > 80 and Cr <= (1.5862*Cb)+20 and
            condition3=False
            if dictTmp["avrjCr"]>135 and dictTmp["avrjCb"]>85 and dictTmp["avrjY"]>80 and dictTmp["avrjCr"]<=((1.5862*dictTmp["avrjCb"])+20):
                condition3=True
            #Cr>=(0.3448*Cb)+76.2069 and Cr >= (-4.5652*Cb)+234.5652 and
            condition4=False
            if dictTmp["avrjCr"]>=((0.3448*dictTmp["avrjCb"])+76.2069) and dictTmp["avrjCr"]>=((-4.5652*dictTmp["avrjCb"])+234.5652):
                condition4=True
            #Cr <= (-1.15*Cb)+301.75 and Cr <= (-2.2857*Cb)+432.85
            condition5=False
            if dictTmp["avrjCr"]<=((-1.15*dictTmp["avrjCb"])+301.75) and dictTmp["avrjCr"]<=((-2.2857*dictTmp["avrjCb"])+432.85):
                condition5=True
            
            #last if
            if condition5 and condition4 and condition3 and condition2 and condition1:
                dictTmp["isSkin"]=True
                

        #paste black box on non skin region
        
        #find posible face area locations
        faces=[]
        #append({"id":x,"left":l,"upper":u,"right":r,"lower":lo})
        #delete smaller areas than avarage  
        faceStats={"aWidth":0,"aHeight":0,"aSize":0}
        #loop through pieces
        for i in range(heightRange):
            for j in range(widthRange):
                dictTmp=pArr[j+(i*widthRange)]
                #find possible skin piece and find other pieces
                if dictTmp["isSkin"] and not dictTmp["isUsed"]:
                    dictTmp["isUsed"]=True
                    #start piece
                    dictTmp2=pArr[j+(i*widthRange)]
                    #left right up and down of piece
                    leftTmp=pArr[j+(i*widthRange)]
                    if (j-1+(i*widthRange))<(heightRange*widthRange):
                        leftTmp=pArr[j-1+(i*widthRange)]
                    rightTmp=pArr[j+(i*widthRange)]
                    if (j+1+(i*widthRange))<(heightRange*widthRange):
                        rightTmp=pArr[j+1+(i*widthRange)]
                    topTmp=pArr[j+(i*widthRange)]
                    if (j+((i+1)*widthRange))<(heightRange*widthRange):
                        topTmp=pArr[j+((i+1)*widthRange)]
                    botTmp=pArr[j+(i*widthRange)]
                    if (j+((i-1)*widthRange))<(heightRange*widthRange):
                        botTmp=pArr[j+((i-1)*widthRange)]
                    #find area width
                    areaWidth=0
                    incrementJ=1
                    while leftTmp["isSkin"] or rightTmp["isSkin"]or topTmp["isSkin"]or botTmp["isSkin"]:
                        areaWidth+=1
                        #check is index out of index
                        if ((j+incrementJ)+(i*widthRange))>=(widthRange*heightRange):
                            break
                        #set current piece as used and go next(horizontally) piece 
                        dictTmp2["isUsed"]=True
                        dictTmp2=pArr[(j+incrementJ)+(i*widthRange)]
                        if (j+incrementJ-1+(i*widthRange))<(widthRange*heightRange):
                            leftTmp=pArr[j+incrementJ-1+(i*widthRange)]
                        if (j+incrementJ+1+(i*widthRange))<(widthRange*heightRange):
                            rightTmp=pArr[j+incrementJ+1+(i*widthRange)]
                        if (j+incrementJ+((i+1)*widthRange))<(widthRange*heightRange):
                            topTmp=pArr[j+incrementJ+((i+1)*widthRange)]
                        if(j+incrementJ+((i-1)*widthRange))<(widthRange*heightRange):
                            botTmp=pArr[j+incrementJ+((i-1)*widthRange)]
                        incrementJ+=1
                    #find area height
                    #start piece
                    dictTmp2=pArr[j+(i*widthRange)]
                    #left right up and down of piece
                    leftTmp=pArr[j+(i*widthRange)]
                    if (j-1+(i*widthRange))<(heightRange*widthRange):
                        leftTmp=pArr[j-1+(i*widthRange)]
                    rightTmp=pArr[j+(i*widthRange)]
                    if (j+1+(i*widthRange))<(heightRange*widthRange):
                        rightTmp=pArr[j+1+(i*widthRange)]
                    topTmp=pArr[j+(i*widthRange)]
                    if (j+((i+1)*widthRange))<(heightRange*widthRange):
                        topTmp=pArr[j+((i+1)*widthRange)]
                    botTmp=pArr[j+(i*widthRange)]
                    if (j+((i-1)*widthRange))<(heightRange*widthRange):
                        botTmp=pArr[j+((i-1)*widthRange)]
                    areaHeigt=0
                    incrementI=1
                    while leftTmp["isSkin"] or rightTmp["isSkin"]or topTmp["isSkin"]or botTmp["isSkin"]:
                        areaHeigt+=1
                        #check is index out of index
                        if (j+((i+incrementI)*widthRange))>=(widthRange*heightRange):
                            break
                        #set current piece as used and go next(vetically) piece
                        dictTmp2["isUsed"]=True
                        dictTmp2=pArr[j+((i+incrementI)*widthRange)]
                        if(j-1+((i+incrementI)*widthRange))<(widthRange*heightRange):
                            leftTmp=pArr[j-1+((i+incrementI)*widthRange)]
                        if(j+1+((i+incrementI)*widthRange))<(widthRange*heightRange):
                            rightTmp=pArr[j+1+((i+incrementI)*widthRange)]
                        if(j+(((i+incrementI)+1)*widthRange))<(widthRange*heightRange):
                            topTmp=pArr[j+(((i+incrementI)+1)*widthRange)]
                        if(j+(((i+incrementI)-1)*widthRange))<(widthRange*heightRange):
                            botTmp=pArr[j+(((i+incrementI)-1)*widthRange)]
                        incrementI+=1
                    
                    #human face ratio width≈5x height≈7x or 0.5<ratio<1.8
                    if areaHeigt>areaWidth and (areaHeigt/areaWidth)<1.8 and (areaHeigt/areaWidth)>0.5 and areaHeigt*areaWidth>(16/factor)*(16/factor):
                        #mark as used pieces inside area
                        uTmp=pArr[j+(i*widthRange)]
                        for x in range(areaWidth):
                            for y in range(areaHeigt):
                                uTmp["isUsed"]=True
                                if (j+x+((i+y)*widthRange))<widthRange*heightRange:
                                    uTmp=pArr[j+x+((i+y)*widthRange)]

                        #print("width "+str(areaWidth)+" height "+str(areaHeigt))
                        left=j*factor
                        upper=i*factor
                        right=j*factor+(factor*areaWidth)
                        lower=i*factor+(factor*areaHeigt)
                        #print("left :"+str(left)+" upper :"+str(upper)+"  right :"+str(right)+" lower:"+str(lower))
                        faces.append({"id":left,"left":left,"upper":upper,"right":right,"lower":lower})
                        faceStats["aWidth"]+=(right-left)
                        faceStats["aHeight"]+=(lower-upper)

        print("total area count ",len(faces))
        #avarage
        faceStats["aWidth"]=faceStats["aWidth"]/len(faces)
        faceStats["aHeight"]=faceStats["aHeight"]/len(faces)
        faceStats["asize"]=faceStats["aHeight"]*faceStats["aWidth"]
        #delete smaller
        delindex=0
        while delindex<len(faces):
            if (faces[delindex]["right"]-faces[delindex]["left"])*(faces[delindex]["lower"]-faces[delindex]["upper"])<faceStats["asize"]:
                del faces[delindex]
                delindex-=1
            delindex+=1
        print("after delete small areas",len(faces))
        #delete same areas
        delId=[]
        for i in range(len(faces)):
            faceStats["aWidth"]+=(faces[i]["right"]-faces[i]["left"])/len(faces)
            faceStats["aHeight"]+=(faces[i]["lower"]-faces[i]["upper"])/len(faces)
            for j in range(len(faces)):
                faceI=faces[i]
                faceJ=faces[j]
                if i != j :
                    #center coordinates
                    ix,iy=faceI["left"]+(faceI["right"]-faceI["left"])/2 , faceI["upper"]+(faceI["lower"]-faceI["upper"])/2
                    jx,jy=faceJ["left"]+(faceJ["right"]-faceJ["left"])/2 , faceJ["upper"]+(faceJ["lower"]-faceJ["lower"])/2
                    #lengths
                    iw,ih=faceI["right"]-faceI["left"] , faceI["lower"]-faceI["upper"]
                    jw,jh=faceJ["right"]-faceJ["left"] , faceJ["lower"]-faceJ["upper"]
                    #if center j inside i 
                    if faceI["right"]>jx and faceI["left"]<jx and faceI["upper"]<jy and faceI["lower"]>jy:
                        #size i> size j delete j
                        if (iw*ih)>(jw*jh):
                            delId.append(faceJ["id"])   
                        elif (iw*ih)<(jw*jh):
                            delId.append(faceI["id"])
        #delete faces
        delindex=0
        while delindex<len(faces):
            if faces[delindex]["id"] in delId:
                del faces[delindex]
                delindex-=1
            delindex+=1
        
        #return face coordinates
        return faces           

    #draw for myFaceDetection
    def drawRectangels(imagePath,faces):        
        #imagename splittedPath[4]
        splittedPath=imagePath.split("/")
        #draw rectangles   
        imageRGB=Image.open(imagePath)
        draw=ImageDraw.Draw(imageRGB)
        for i in range(len(faces)):
            faceTmp=faces[i]
            draw.rectangle(((faceTmp["left"],faceTmp["upper"]),(faceTmp["right"],faceTmp["lower"])),outline=(255,0,0))
        del draw
        imageRGB.save('./uploadedImages/proccesed/proccesed'+splittedPath[4])
        return './uploadedImages/proccesed/proccesed'+splittedPath[4]