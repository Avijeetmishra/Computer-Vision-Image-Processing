# -*- coding: utf-8 -*-
import numpy as np
import cv2
import math

#Create Gx and Gy
x1 = np.array((1,2,1))
x1 = np.reshape(x1,[3,1])
x2 = np.array((-1,0,1))
x2 = np.reshape(x2,[1,3])
y1 = np.array((-1,0,1))
y1 = np.reshape(y1,[3,1])
y2 = np.array((1,2,1))
y2 = np.reshape(y2,[1,3])

# Load an color image in grayscale
img = cv2.imread('lena_gray.jpg',0)
#Add padding
cv2.copyMakeBorder(img,1,1,1,1,cv2.BORDER_REPLICATE)
#Initialize Gx and Gy
Gx= np.zeros((514,514))
Gy= np.zeros((514,514))
Gx1= np.zeros((514,514))
Gy1= np.zeros((514,514))
Gmag= np.zeros((514,514))

for indx in range(1,511):
    for indy in range(1,511):
        Gx[indx,indy]= img[indx-1,indy]*x1[0,0] + img[indx,indy]*x1[1,0] + img[indx+1,indy]*x1[2,0]

        Gy[indx,indy]= img[indx-1,indy]*y1[0,0] + img[indx,indy]*y1[1,0] + img[indx+1,indy]*y1[2,0]
        
for indx in range(1,511):
    for indy in range(1,511):
        Gx1[indx,indy]= Gx[indx,indy-1]*x2[0,0] + Gx[indx,indy]*x2[0,1] + Gx[indx,indy+1]*x2[0,2]

        Gy1[indx,indy]= Gy[indx,indy-1]*y2[0,0] + Gy[indx,indy]*y2[0,1] + Gy[indx,indy+1]*y2[0,2]
        
        #Gmag[indx,indy]= math.sqrt(((Gx1[indx,indy]/688.00)*(Gx1[indx,indy]/688.00))+((Gy1[indx,indy]/644.00)*(Gy1[indx,indy]/644.00)))


maxx = np.amax(Gx1)
maxy = np.amax(Gy1)

Gxdis = Gx1/maxx
Gxdis = np.abs(Gxdis)
Gydis = Gy1/maxy
Gydis = np.abs(Gydis)

for indx in range(1,511):
    for indy in range(1,511):
        Gmag[indx,indy]= math.sqrt((Gx1[indx,indy]*Gx1[indx,indy])+(Gy1[indx,indy]*Gy1[indx,indy]))
#Gmag= math.sqrt((Gx*Gx)+(Gy*Gy))
maxmag = Gmag.max()
Gmag = Gmag/maxmag
Gmag = np.abs(Gmag)

cv2.namedWindow('Gx1', cv2.WINDOW_NORMAL)
cv2.namedWindow('Gy1', cv2.WINDOW_NORMAL)
cv2.namedWindow('Gmag1', cv2.WINDOW_NORMAL)
#Ximg = cv2.Sobel(img,-1, 0,1,3)


cv2.imshow('Gx1',Gxdis)
cv2.imshow('Gy1',Gydis)
cv2.imshow('Gmag1',Gmag)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
