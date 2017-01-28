import numpy as np
import cv2
import math
from matplotlib import pyplot as plt

img= cv2.imread('sharat.jpg',0)
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.imshow('Image',img)

H=np.zeros((1,256))
Hc=np.zeros((1,256))
T=np.zeros((1,256))
F=np.zeros((1,256))

#Compute Image histogram
for indx in range(0,256):
    for indy in range(0,256):
        temp = img[indx][indy]
        H[0][temp] = H[0][temp] + 1
            
         
#Plot Image Histogram corresponding to H
plt.figure('Image Histogram corresponding to H')
plt.plot(np.transpose(H))
plt.show()

# Compute Cumulative Image Histogram and Transformation Function

Hc[0][0]= H[0][0]
for indy in range(1,255):
    Hc[0][indy]=Hc[0][indy-1] + H[0][indy]
    T[0][indy]= round((255 * Hc[0][indy])/(256*256)) 

#Plot Cumulative Histogram corresponding to H
plt.figure('Cumulative Histogram corresponding to H')
plt.plot(np.transpose(Hc))
plt.show()

#Plot Transformation Function
plt.figure('Transformation Function')
plt.plot(np.transpose(T))
plt.show() 

#Enhance Image
for i in range(0,255):
    for j in range(0,255):
           # for x in range(0,256):
        temp1 = img[i][j]
        img[i][j] = T[0][temp1]

cv2.namedWindow('Enhanced Image', cv2.WINDOW_NORMAL)
cv2.imshow('Enhanced Image', img)

#Plot Final Image Histogram
for i in range(1,255):
    for j in range(1,255):
        temp2 = T[0][j]
        F[0][temp2] = F[0][temp2] + 1
                        
plt.figure('Final Histogram Image')
plt.plot(np.transpose(F))
plt.show()

