import cv2
import numpy as np

left_img = cv2.imread('view1.png', 0)  #read it as a grayscale image
right_img = cv2.imread('view5.png', 0)

#Disparity Computation for Left Image
#left_img = cv2.copyMakeBorder(left_img,4,4,4,4,cv2.BORDER_REPLICATE)
#D_L = np.zeros(370,463)
#D_R = np.zeros(370,463)
#OcclusionCost = 20 (You can adjust this, depending on how much threshold you want to give for noise)
Occlusion = 20
#For Dynamic Programming you have build a cost matrix. Its dimension will be numcols x numcols

#CostMatrix = zeros(numcols,numcols)
#DirectionMatrix = zeros(numcols,numcols)  (This is important in Dynamic Programming. You need to know which direction you need traverse)
#We first populate the first row and column values of Cost Matrix

#for(i=0; i < numcols; i++)
#      CostMatrix(i,0) = i*OcclusionCost
#      CostMatrix(0,i) = i*OcclusionCost


# Now, its time to populate the whole Cost Matrix and DirectionMatrix
D = np.zeros((370,463))
Dr = np.zeros((370,463))
# Use the pseudocode from "A Maximum likelihood Stereo Algorithm" paper given as reference
for l in range(0,370):
    print l
    C = np.zeros((463,463)) 
    for p in range(0,463):
        C[p,0] = p*Occlusion
        C[0,p] = p*Occlusion
        
    M = np.zeros((463,463))
    Mr = np.zeros((463,463))
    for i in range(0,463):
        for j in range(0,463):

            min1 = C[i-1,j-1] + np.abs(left_img[l,i] - right_img[l,j])    #cost
            min2 = C[i-1,j] + Occlusion
            min3 = C[i,j-1] + Occlusion
            if(min1>min2):
                cmin = min2
            else:
                cmin = min1
            if(min3<cmin):
                cmin = min3
                M[i,j] = 3
            else:
                if(min1==cmin):
                    M[i,j] = 1
                else:
                    M[i,j] = 2
                
            C[i,j] = cmin
            
    p,q = 462,462
    while((p!=0) and (q!=0)):
        if(M[p,q] == 1):
            D[l,p] = np.abs(p-q)
            Dr[l,q] = np.abs(p-q)
            p = p-1
            q = q-1
        else:
            if(M[p,q] == 2):
                p = p-1
                D[l,p] = 0
                Dr[l,q] = 0
            else:
                q = q-1
                D[l,p] = 0
                Dr[l,q] = 0
    
cv2.namedWindow('Dl', cv2.WINDOW_NORMAL)
cv2.imshow('Dl',D/D.max())

cv2.namedWindow('Dr', cv2.WINDOW_NORMAL)
cv2.imshow('Dr',Dr/Dr.max())


