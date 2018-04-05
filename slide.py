import predictor
import numpy as np
import os,glob,cv2
import sys,argparse
import os.path
import math


image_size=128
num_channels=3
#image_path = 'C:\\Users\\senura\\Desktop\\452project\\imgrec\\proj\\'

dir_path = os.path.dirname(os.path.realpath(__file__))
image_path=sys.argv[1] 
filename = dir_path +'/' +image_path



def getimage(filename):
    image = cv2.imread(filename)
    
    row = image.shape[0]
    col = image.shape[1]
    
    return image,row,col
	
	
def slidingwindow(image,row,col,image_size,num_channels):
    row_img = []
    col_img = []
    xycoords = []
    probs =[]
    x = row%13
    x = 13-x
    row = row+x
    y = col%13
    y = 13-y 
    col = col+y
    image = cv2.resize(image, (col, row),0,0, cv2.INTER_LINEAR)
    print(row)
    z = 1
    r = row/13
    q = col/13
    image = np.array(image)
    print(r,q)
    row = math.floor(r)
    col = math.floor(q)
    first = 0
    second = 0
    third = 0
    fourth = 0
    print(image.shape)
    coords = ['x','y']
    for j in range (13):
        for i in range(13): 
            global first
            global second
            global fourth
            global third
            print(i, j)
            first,second,third,fourth,c  = getcoords(i,j,first,second,third,fourth)
            image_out = image[first:second,third:fourth,0:3]
            images = predictor.preprocess(image_size, image_out)
            probability , x =  predictor.predict(image,images,image_size,num_channels,z)
            probs.append(probability)
            print(probability)
            row_img.append(x)
            #print(image_out)
        col_img.append(row_img)
        xycoords.append(c)
        
    #total = totalprobability/13*13
    return probs , z
            
    

               
j = 0
def getcoords(x, y,first,second,third,fourth):
   
    global j 
    first = 0
    second = 128
    third = 0
    fourth = 188
    coordinates = []
    first = first + second*y
    second = second + second*y
    third = third +fourth*x 
    fourth = fourth + fourth*x
    
    c = x,y
    coordinates.append(c)
    c = np.array(c)
    #print(first,second,third,fourth)
    
    
    return first,second,third,fourth , c
	
image,row,col = getimage(filename)
total,z = slidingwindow(image,row,col,image_size,num_channels)
print (totalprobability)

print(z)

