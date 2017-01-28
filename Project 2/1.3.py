import numpy as np
import cv2
from matplotlib import pyplot as plt

imgL = cv2.imread('view1.png',1)
imgR = cv2.imread('view5.png',1)

gtL = cv2.imread('disp1.png',1)
gtR = cv2.imread('disp5.png',1)

Hl= np.zeros((370,463,3))
Hr= np.zeros((370,463,3))
Hr1= np.zeros((370,463,3))
Hrf= np.zeros((370,463,3))
Hrf1= np.zeros((370,463,3))
Hf= np.zeros((370,463,3))
for m in range(0,370):
    #print m
    for n in range(0,463):
        valfr = gtL[m,n,0]/2

        valfr = int(valfr)
        
        if(n-valfr>0):
            
            Hl[m,n-valfr,0] = imgL[m,n,0]
            Hl[m,n-valfr,1] = imgL[m,n,1]
            Hl[m,n-valfr,2] = imgL[m,n,2]
        
        if(n+valfr<463):
            Hr[m,n+valfr,0] = imgR[m,n,0]
            Hr[m,n+valfr,1] = imgR[m,n,1]
            Hr[m,n+valfr,2] = imgR[m,n,2]

for m in range(0,370):
    #print m
    for n in range(0,463):
       if(Hl[m,n,0]== 0):
            if(Hl[m,n,0]== 0):
                Hrf[m,n  ,0] = Hr[m,n,0]
            if(Hl[m,n,1]== 0):            
                Hrf[m,n  ,1] = Hr[m,n,1]
            if(Hl[m,n,2]== 0):
                Hrf[m,n  ,2] = Hr[m,n,2]

for m in range(0,370):
    for n in range(0,463):
        Hl[m,n,0] = Hl[m,n,0] + Hrf[m,n,0]
        Hl[m,n,1] = Hl[m,n,1] + Hrf[m,n,1,]
        Hl[m,n,2] = Hl[m,n,2] + Hrf[m,n,2]
for m in range(0,370):
    for n in range(0,463):
        valfr = gtL[m,n,0]/2
        if(n-valfr>0):
            if(Hl[m,n,0]== 0 and Hl[m,n,1]== 0 and Hl[m,n,2]== 0):
                Hrf1[m,n  ,0] = imgR[m,n -valfr,0]
                Hrf1[m,n  ,1] = imgR[m,n -valfr,1] 
                Hrf1[m,n  ,2] = imgR[m,n -valfr,2]

for m in range(0,370):
    for n in range(0,463):
        Hf[m,n,0] = Hl[m,n,0] + Hrf1[m,n,0]
        Hf[m,n,1] = Hl[m,n,1] + Hrf1[m,n,1]
        Hf[m,n,2] = Hl[m,n,2] + Hrf1[m,n,2]
            

cv2.namedWindow('Final Image', cv2.WINDOW_NORMAL)
cv2.imshow('Final Image',Hf/Hf.max())
