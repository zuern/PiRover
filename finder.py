import numpy as np
import os,glob,cv2
import sys,argparse
import os.path
from sklearn.utils import shuffle


classes = ['cars','not_car']
train_path = 'training_data'
validation_size = 0.2
image_size = 128

def importtrainset(train_path, image_size, classes):
    images = []
    labels = []
    
    
    for fields in classes:   
        index = classes.index(fields)
        print('reading files')
        path = os.path.join(train_path, fields, '*g')
        files = glob.glob(path)
        for fl in files:
            image = cv2.imread(fl)
            image = cv2.resize(image, (image_size, image_size),0,0, cv2.INTER_LINEAR)
            image = image.astype(np.float32)
            image = np.multiply(image, 1.0 / 255.0)
            images.append(image)
            label = np.zeros(len(classes))
            label[index] = 1.0
            #print(label)
            labels.append(label)
    images = np.array(images)
    labels = np.array(labels)
	
    return images, labels


#split validation set and train set
def readandvalidate(validation_size,image_size,images, labels):
 

    if isinstance(validation_size, float):
      validation_size = int(validation_size * images.shape[0])
  

    validation_images = images[:validation_size]
    validation_labels = labels[:validation_size]
    train_images = images[validation_size:]
    train_labels = labels[validation_size:]


 
    return validation_images, validation_labels, train_images, train_labels


def sendtrain32(train_images, train_labels,ep):
    
    start, end = getstartend(ep)
    
    return  train_images[start:end], train_labels[start:end]

def sendval32(validation_images, validation_labels,xp):
    
    start, end = getstartend(xp)
    
    return  validation_images[start:end], validation_labels[start:end]

	
def getstartend(ep):
    #print (ep)
    if (ep > 30):
        start = 0
        end = 0
        
    start = 32*ep
    #print (start)
    end = 32 + 32*ep
    #print (start,end)
    return start ,end       

    


