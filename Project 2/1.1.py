import numpy as np
import cv2
from matplotlib import pyplot as plt

imgL = cv2.imread('view1.png',0)
imgR = cv2.imread('view5.png',0)

gtL = cv2.imread('disp1.png',0)
gtR = cv2.imread('disp5.png',0)

#imgL = cv2.copyMakeBorder(imgL,4,4,4,4,cv2.BORDER_REPLICATE)
#imgR = cv2.copyMakeBorder(imgR,4,4,4,4,cv2.BORDER_REPLICATE)
#gtL = cv2.copyMakeBorder(gtL,4,4,4,4,cv2.BORDER_REPLICATE)
#gtR = cv2.copyMakeBorder(gtR,4,4,4,4,cv2.BORDER_REPLICATE)
Hx3= np.zeros((370,463))
Hy3= np.zeros((370,463))
Hx9= np.zeros((370,463))
Hy9= np.zeros((370,463))

bpl3 = np.zeros((370,463))
bpr3 = np.zeros((370,463))
bpl9 = np.zeros((370,463))
bpr9 = np.zeros((370,463))
temp = 0
temp1 = 0
temp2 = 0
temp3 = 0

for m in range(0,370):
    print m
    for n in range(0,463):
     #   o = n
        #if(n>5):
      #      o = 5
        match=0
        match1=0
        match2=0
        match3=0
        min_ssd  = 5308416
        min_ssd1 = 5308416
        min_ssd2 = 5308416
        min_ssd3 = 5308416
        
        #Left 9x9
        o = n
        while(o>0 and o!= n-75):
            temp =0
            for k in range(-4,5):
                for l in range(-4,5):
                    if(463>n-l>-1 and 370>m-k>-1):
                        temp = temp + np.square(imgL[m-k,n-l] - imgR[m-k,o-l])
            if(temp<min_ssd):
                min_ssd = temp
                match = o
        #Left 3x3
            temp2 =0
            for k in range(-1,2):
                for l in range(-1,2):
                    if(463>n-l>-1 and 370>m-k>-1):
                        temp2 = temp2 + np.square(imgL[m-k,n-l] - imgR[m-k,o-l])
            if(temp2<min_ssd2):
                min_ssd2 = temp2
                match2 = o
            o = o-1
            
        #Right 9x9
        o = n
        while(o<463 and o!= n+75):
            temp1 =0
            for k in range(-4,5):
                for l in range(-4,5):
                    if(463>o+l>-1 and 370>m+k>-1):
                        temp1 = temp1 + np.square(imgR[m+k,n+l] - imgL[m+k,o+l])
            if(temp1<min_ssd1):
                min_ssd1 = temp1
                match1 = o
           
        
        #Right 3x3
            temp3 =0
            for k in range(-1,2):
                for l in range(-1,2):
                    if(463>o+l>-1 and 370>m+k>-1):
                        temp3 = temp3 + np.square(imgR[m+k,n+l] - imgL[m+k,o+l])
            if(temp3<min_ssd3):
                min_ssd3 = temp3
                match3 = o
            o = o+1

   
                
        Hx3[m,n] = n - match2
        Hy3[m,n] = match3 - n            
        Hx9[m,n] = n - match
        Hy9[m,n] = match1 - n            

MSE1 = 0
MSE2 = 0
MSE3 = 0
MSE4 = 0
for m in range(0,370):
    for n in range(0,463):
        MSE1 = MSE1 + np.square(gtL[m,n] - Hx9[m,n])
        MSE2 = MSE2 + np.square(gtR[m,n] - Hy9[m,n])
        MSE3 = MSE3 + np.square(gtL[m,n] - Hx3[m,n])
        MSE4 = MSE4 + np.square(gtR[m,n] - Hy3[m,n])
MSE1 = MSE1/(370*463)
MSE2 = MSE2/(370*463)
MSE3 = MSE3/(370*463)
MSE4 = MSE4/(370*463)

print 'MSE for Disparity left 9x9 : ' + str(MSE1) 
print 'MSE for Disparity  right 9x9 : ' + str(MSE2)  
print 'MSE for Disparity  left 3x3 : ' + str(MSE3)      
print 'MSE for Disparity  right 3x3 : ' + str(MSE4)

for m in range(0,370):
    for n in range(0,463):
        #back projection left 9x9
        val = Hx9[m,n]
        if(463>n-val>-1):
            if(val != Hy9[m,n-val]):
                bpl9[m, n] = 0
            else:
                bpl9[m, n] = Hx9[m,n]
        #back projection right 9x9
        val = Hy9[m,n]
        if(463>n+val>-1):
            if(val != Hx9[m,n+val]):
                bpr9[m, n] = 0
            else:
                bpr9[m, n] = Hy9[m,n]
        
        #back projection left 3x3        
        val = Hx3[m,n]
        if(463>n-val>-1):
            if(val != Hy3[m,n-val]):
                bpl3[m, n] = 0
            else:
                bpl3[m, n] = Hx3[m,n]
        #back projection left 3x3
        val = Hy3[m,n]
        if(463>n+val>-1):
            if(val != Hx3[m,n+val]):
                bpr3[m, n] = 0
            else:
                bpr3[m, n] = Hy3[m,n]
        
MSE1 = 0
MSE2 = 0
MSE3 = 0
MSE4 = 0
for m in range(0,370):
    for n in range(0,463):
        if bpl9[m,n]!=0:
            MSE1 = MSE1 + np.square(gtL[m,n] - bpl9[m,n])
        if bpr9[m,n]!=0:    
            MSE2 = MSE2 + np.square(gtR[m,n] - bpr9[m,n])
        if bpl3[m,n]!=0:
            MSE3 = MSE3 + np.square(gtL[m,n] - bpl3[m,n])
        if bpr3[m,n]!=0:    
            MSE4 = MSE4 + np.square(gtR[m,n] - bpr3[m,n])
MSE1 = MSE1/(370*463)
MSE2 = MSE2/(370*463)
MSE3 = MSE3/(370*463)
MSE4 = MSE4/(370*463)

print 'MSE for back projection left 9x9 : ' + str(MSE1) 
print 'MSE for back projection right 9x9 : ' + str(MSE2)  
print 'MSE for back projection left 3x3 : ' + str(MSE3)      
print 'MSE for back projection right 3x3 : ' + str(MSE4)

cv2.namedWindow('Left Disparity 3x3', cv2.WINDOW_NORMAL)
cv2.imshow('Left Disparity 3x3',Hx3/Hx3.max())
cv2.namedWindow('Right Disparity 3x3', cv2.WINDOW_NORMAL)
cv2.imshow('Right Disparity 3x3',Hy3/Hy3.max())
cv2.namedWindow('Left Disparity 9x9', cv2.WINDOW_NORMAL)
cv2.imshow('Left Disparity 9x9',Hx9/Hx9.max())
cv2.namedWindow('Right Disparity 9x9', cv2.WINDOW_NORMAL)
cv2.imshow('Right Disparity 9x9',Hy9/Hy9.max())

cv2.namedWindow('back projection left 3x3', cv2.WINDOW_NORMAL)
cv2.imshow('back projection left 3x3',bpl3/bpl3.max())
cv2.namedWindow('back projection right 3x3', cv2.WINDOW_NORMAL)
cv2.imshow('back projection right 3x3',bpr3/bpr3.max())
cv2.namedWindow('back projection left 9x9', cv2.WINDOW_NORMAL)
cv2.imshow('back projection left 9x9',bpl9/bpl9.max())
cv2.namedWindow('back projection right 9x9', cv2.WINDOW_NORMAL)
cv2.imshow('back projection right 9x9',bpr9/bpr9.max())