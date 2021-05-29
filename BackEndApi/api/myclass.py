from PIL import Image
import base64
from io import BytesIO
import numpy as np
class MyClass():
    def __init__(self,image):
        self.image=image
    #dlib detect faces
    def showImage(b64str):
        im = Image.open(BytesIO(base64.b64decode(b64str)))
        im.show()
        print(im.size)
        return 0
    #is skin
    def isSkin(rgb,ycbcr,hsv,width,height):
        #output boolean array
        output=np.zeros((height,width),dtype=bool)
        #rgb arrays
        r,g,b=rgb[...,0],rgb[...,1],rgb[...,2]
        #ycbcr arrays
        y,cb,cr=ycbcr[...,0],ycbcr[...,1],ycbcr[...,2]
        #hsv arrays
        h,s,v=hsv[...,0],hsv[...,1],hsv[...,2]
        #threshold
        threshold = (r>95) & (g>40) & (b>20) & (r>g) & (r>b) & (np.abs(r-g)>15) & (cr>135) & (cb>85) & (y>80) & (cr<=((1.5862*cb)+20)) & (cr>=((0.3448*cb)+76.2069)) & (cr>=((-4.5652*cb)+234.5652)) & (cr<=((-1.15*cb)+301.75)) & (cr<=((-2.2857*cb)+432.85))
        #threshold = ((r>95) & (g>40) & (b>20) & (r>g) & (r>b) & (np.abs(r-g)>15) & (cr>135) & (cb>85) & (y>80) & (cr<=((1.5862*cb)+20)) & (cr>=((0.3448*cb)+76.2069)) & (cr>=((-4.5652*cb)+234.5652)) & (cr<=((-1.15*cb)+301.75)) & (cr<=((-2.2857*cb)+432.85))) | ((h>=0) & (h<=50) & (s>=0.23) & (s<=0.68) & (r>95) & (g>40) & (b>20) & (r>g) & (r>b) & (np.abs(r-g)>15))
        output[np.where(threshold)]=True    
        return output
    #returns face locations as dictionary list[{"id":x,"left":l,"upper":u,"right":r,"lower":lo})]
    def detectFaces(b64img):    
        #RGB
        imageRGB=Image.open(BytesIO(base64.b64decode(b64img)))#Image.open(imagePath)
        rgbPixels=np.array(imageRGB)
        #YCbCr
        imageYCBCR=imageRGB.convert('YCbCr')#Image.open(imagePath).convert('YCbCr')
        ycbcrPixels=np.array(imageYCBCR)
        #HSV
        imageHSV=imageRGB.convert('HSV')
        hsvPixels=np.array(imageHSV)
        #is skin?
        boolArr=MyClass.isSkin(rgbPixels,ycbcrPixels,hsvPixels,imageRGB.width,imageRGB.height)    
        #blobs
        blobs=MyClass.findblobs(boolArr)
        #find biggest blob
        bigBlob=MyClass.getBiggest(blobs)
        return bigBlob
    #twopass
    def findblobs(arr):
        height,width=arr.shape
        #used pixels
        used=np.ones((height,width),dtype=bool)
        #append({"left":l,"upper":u,"right":r,"lower":lo})
        blobs=[]
                    
        limit=200
        #1st pass
        for r in range(height-limit):
            for c in range(width-limit):
                dim=100
                #if pixel is skin    
                if arr[r,c] and used[r,c]:
                    count=MyClass.countNeighbors(arr[r:r+dim,c:c+dim])
                    while (count/(dim*dim))>0.3 and dim<400:
                        count=MyClass.countNeighbors(arr[r:r+dim,c:c+dim])
                        dim+=20
                    xxxx=dim*dim
                    #append
                    if (count/xxxx)>0.2:
                        #print("height",blobHeight,"        width",blobWidth)
                        blobs.append({"dim":dim,"left":c,"upper":r,"right":c+dim,"lower":r+dim})
                        #fill inside blob
                        used[r:r+dim,c:c+dim]=False
                        arr[r:r+dim,c:c+dim]=False
        
        return blobs
    
    #count skin pixel in area
    def countNeighbors(neighbors):
        count=np.count_nonzero(neighbors)
        return count
    #get biggest blob
    def getBiggest(blobs):
        max=0
        blob=0
        for i in range(len(blobs)):
            faceTmp=blobs[i]
            if faceTmp["dim"]>max:
                max=faceTmp["dim"]
                blob=faceTmp
        return blob 