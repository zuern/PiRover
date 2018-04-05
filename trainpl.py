import finder
import tensorflow as tf
import time
from datetime import timedelta
import math
import random
import numpy as np
from sklearn.utils import shuffle


from numpy.random import seed
seed(1)
from tensorflow import set_random_seed
set_random_seed(2)


batch_size = 32

#input classes
classes = ['cars','not_car']
num_classes = len(classes)

# 25% val set
validation_size = 0.25
img_size = 128
num_channels = 3
train_path='training_data'

images, labels = finder.importtrainset(train_path, img_size, classes)
images, labels = shuffle(images, labels)
data = [images,labels]
validation_images, validation_labels, train_images,train_labels = finder.readandvalidate(validation_size,img_size,images, labels)


print("length of validation set:",len(validation_images))
print(len(validation_labels))
print("length of train set:",len(train_images))
print(len(train_labels))



session = tf.Session()
x = tf.placeholder(tf.float32, shape=[None, img_size,img_size,num_channels], name='x')

## labels
y_true = tf.placeholder(tf.float32, shape=[None, num_classes], name='y_true')
y_true_cls = tf.argmax(y_true, dimension=1)



##Net parameters
filter_size_conv1 = 3 
num_filters_conv1 = 32

filter_size_conv2 = 3
num_filters_conv2 = 32

filter_size_conv3 = 3
num_filters_conv3 = 64
    
fc_layer_size = 128

def create_weights(shape):
    return tf.Variable(tf.truncated_normal(shape, stddev=0.05))

def create_biases(size):
    return tf.Variable(tf.constant(0.05, shape=[size]))



def create_convolutional_layer(input,  num_input_channels, conv_filter_size, num_filters):  
    
    ## define weights and biases
    weights = create_weights(shape=[conv_filter_size, conv_filter_size, num_input_channels, num_filters])
    
    biases = create_biases(num_filters)

    ## CC layer
    layer = tf.nn.conv2d(input=input,  filter=weights, strides=[1, 1, 1, 1], padding='SAME')

    layer += biases

    ## maxpooling 
    layer = tf.nn.max_pool(value=layer, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1],padding='SAME')
    ## relu
    layer = tf.nn.relu(layer)

    return layer

    

def create_flatten_layer(layer):
    #shape of the layer will be [batch_size img_size img_size num_channels] 
    
    layer_shape = layer.get_shape()

    ## No. features is img_height * img_width* num_channels.
    num_features = layer_shape[1:4].num_elements()

    ## flatten
    layer = tf.reshape(layer, [-1, num_features])

    return layer


def create_fc_layer(input,num_inputs, num_outputs,use_relu=True):
    
    #weights and biases.
    weights = create_weights(shape=[num_inputs, num_outputs])
    biases = create_biases(num_outputs)

    # Fully connected layer 
    layer = tf.matmul(input, weights) + biases
    if use_relu:
        layer = tf.nn.relu(layer)

    return layer


layer_conv1 = create_convolutional_layer(input=x, num_input_channels=num_channels,conv_filter_size=filter_size_conv1, num_filters=num_filters_conv1)

layer_conv2 = create_convolutional_layer(input=layer_conv1, num_input_channels=num_filters_conv1, conv_filter_size=filter_size_conv2, num_filters=num_filters_conv2)

layer_conv3= create_convolutional_layer(input=layer_conv2, num_input_channels=num_filters_conv2, conv_filter_size=filter_size_conv3, num_filters=num_filters_conv3)
          
layer_flat = create_flatten_layer(layer_conv3)

layer_fc1 = create_fc_layer(input=layer_flat, num_inputs=layer_flat.get_shape()[1:4].num_elements(),  num_outputs=fc_layer_size,use_relu=True)

layer_fc2 = create_fc_layer(input=layer_fc1,  num_inputs=fc_layer_size, num_outputs=num_classes,  use_relu=False) 

y_pred = tf.nn.softmax(layer_fc2,name='y_pred')
y_pred_cls = tf.argmax(y_pred, dimension=1)


session.run(tf.global_variables_initializer())
cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=layer_fc2, labels=y_true)
cost = tf.reduce_mean(cross_entropy)
optimizer = tf.train.AdamOptimizer(learning_rate=1e-4).minimize(cost)
correct_prediction = tf.equal(y_pred_cls, y_true_cls)
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))


session.run(tf.global_variables_initializer()) 


def show_progress(epoch, feed_dict_train, feed_dict_validate, val_loss):
    acc = session.run(accuracy, feed_dict=feed_dict_train)
    val_acc = session.run(accuracy, feed_dict=feed_dict_validate)
    
    print("Training Epoch" ,epoch, " Training Accuracy: ",acc, " Validation Accuracy: ", val_acc, " Validation Loss:",val_acc)
    return

total_iterations = 0
ep = 0
xp = 0
saver = tf.train.Saver()
def train(num_iteration):
    global total_iterations
    global ep
    global xp
    for i in range(total_iterations, total_iterations + num_iteration):
        
        
        x_batch, y_true_batch = finder.sendtrain32(train_images =train_images,train_labels = train_labels, ep = ep)
        x_valid_batch, y_valid_batch = finder.sendval32(validation_images = validation_images, validation_labels = validation_labels, xp = xp)
        #print(x_batch[1])
        ep = ep +1
        xp = xp +1
        #print ("new")
        if (ep > 10):
            ep = np.random.randint(0,23)
        if (xp > 8):
            xp = np.random.randint(0,4)
       
        #print(y_true_batch)
        
        feed_dict_tr = {x: x_batch, y_true: y_true_batch}
        feed_dict_val = {x: x_valid_batch, y_true: y_valid_batch}

        session.run(optimizer, feed_dict=feed_dict_tr)

        if i % int(images.shape[0]/batch_size) == 0: 
            val_loss = session.run(cost, feed_dict=feed_dict_val)
            epoch = int(i / int(images.shape[0]/batch_size))    
            
            show_progress(epoch, feed_dict_tr, feed_dict_val, val_loss)
            saver.save(session, 'C:\\Users\\senura\\Desktop\\452project\\imgrec\\proj\\cars-model') 


    total_iterations += num_iteration

train(num_iteration=2000)
