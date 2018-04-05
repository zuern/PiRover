import tensorflow as tf
import numpy as np
import cv2







def preprocess(image_size,image):
    images = []
    print(image.shape)
    im = cv2.resize(image, (image_size, image_size),0,0, cv2.INTER_LINEAR)
    images.append(im)
    images = np.array(images, dtype=np.uint8)
    images = images.astype('float32')
    images = np.multiply(images, 1.0/255.0) 
    return images
	

def predict(image,images,image_size,num_channels,c):
    x_batch = images.reshape(1, image_size,image_size,num_channels)




    sess = tf.Session()
    saver = tf.train.import_meta_graph('cars-model.meta')
    saver.restore(sess, tf.train.latest_checkpoint('./'))

    graph = tf.get_default_graph()

    y_pred = graph.get_tensor_by_name("y_pred:0")

    x= graph.get_tensor_by_name("x:0") 
    y_true = graph.get_tensor_by_name("y_true:0") 
    y_test_images = np.zeros((1, 2)) 



    feed_dict_testing = {x: x_batch, y_true: y_test_images}

    result=sess.run(y_pred, feed_dict=feed_dict_testing)
    r = result[0]
    car = r[0]
    notcar = r[1]

    

    
    probcar = r[0]
    if (probcar < 0.3):
        c = 0
        drawbox(image,images)
        #print(images)
    else:
        c = 1
    return probcar,c


def drawbox(image,images):
    print(images.shape)
    #cv2.line(image,images,(255,0,0),5)
    #cv2.imshow('image',imgage)
