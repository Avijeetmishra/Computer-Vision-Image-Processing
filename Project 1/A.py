# -*- coding: utf-8 -*-
import numpy as np
import cv2
import math

#Create Gx and Gy
x = np.array((-1,0,1,-2,0,2,-1,0,1))
x = np.reshape(x,[3,3])
y = np.array((-1,-2,-1,0,0,0,1,2,1))
y = np.reshape(y,[3,3])

# Load an color image in grayscale
img = cv2.imread('lena_gray.jpg',0)
#Add padding
cv2.copyMakeBorder(img,1,1,1,1,cv2.BORDER_REPLICATE)
#Initialize Gx and Gy
Gx= np.zeros((514,514))
Gy= np.zeros((514,514))
Gmag= np.zeros((514,514))

maxx = 0
maxy = 0
for indx in range(1,511):
    for indy in range(1,511):
        Gx[indx,indy]= img[indx-1,indy-1]*x[0,0] + img[indx-1,indy]*x[0,1] + img[indx-1,indy+1]*x[0,2] + img[indx,indy-1]*x[1,0] + img[indx,indy]*x[1,1] + img[indx,indy+1]*x[1,2] + img[indx+1,indy-1]*x[2,0] + img[indx+1,indy]*x[2,1] + img[indx+1,indy+1]*x[2,2] 

        Gy[indx,indy]= img[indx-1,indy-1]*y[0,0] + img[indx-1,indy]*y[0,1] + img[indx-1,indy+1]*y[0,2] + img[indx,indy-1]*y[1,0] + img[indx,indy]*y[1,1] + img[indx,indy+1]*y[1,2] + img[indx+1,indy-1]*y[2,0] + img[indx+1,indy]*y[2,1]+ img[indx+1,indy+1]*y[2,2] 

maxx = np.amax(Gx)
maxy = np.amax(Gy)

Gxdis = Gx/maxx
Gxdis = np.abs(Gxdis)
Gydis = Gy/maxy
Gydis = np.abs(Gydis)

for indx in range(1,511):
    for indy in range(1,511):
        Gmag[indx,indy] = math.sqrt((Gx[indx,indy]*Gx[indx,indy])+(Gy[indx,indy]*Gy[indx,indy]))

maxmag = Gmag.max()
Gmag = Gmag/maxmag
Gmag = np.abs(Gmag)



#Gmag= math.sqrt((Gx*Gx)+(Gy*Gy))
cv2.namedWindow('Gx', cv2.WINDOW_NORMAL)
cv2.namedWindow('Gy', cv2.WINDOW_NORMAL)
cv2.namedWindow('Gmag', cv2.WINDOW_NORMAL)
#Ximg = cv2.Sobel(img,-1, 0,1,3)


cv2.imshow('Gx',Gxdis)
cv2.imshow('Gy',Gydis)
cv2.imshow('Gmag',Gmag)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
