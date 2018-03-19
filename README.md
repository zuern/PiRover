# PiRover
PiRover will be a small robot to be built using electronic components from QKits Kingston. The robot will use object detection via a convolutional neural network to identify and drive towards a target object (a banana) in the environment. The robot will consist of:
- A Raspberry Pi (already owned)
- A robot chassis kit QKits Link
- A Raspberry Pi compatible camera QKits Link
- 2 battery packs (For powering the Pi and Motors seperately)
- USB Wireless Adapter
- DC Motor Control Board (2 H-Bridge Circuits) QKits Link 

We are working on two different implementations for the object detector CNN:
**Method 1:**
Divide the image into an NxN grid. Pass an image classifier trained on the target object over each grid square. The square with highest activation is designated to contain the target object.
This method will output a coarse bounding box, however the implementation is simple. This method can be optimized by manipulating values of N to find the best grid square-size.

**Method 2:**
Our second method will be using the YOLO (You Only Look Once) algorithm for object detection.  This functions by determining the “best” locations for bounding boxes, and then passing these regions to the classifier. This happens with only one pass through the CNN and is highly performant.

