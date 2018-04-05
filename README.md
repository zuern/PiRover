# PiRover
PiRover is a small robot built using electronic components from QKits Kingston. The robot uses object detection via a convolutional neural network to identify a target in the environment (a toy car) and drive towards it. The robot consists of:
- A Raspberry Pi
- A robot chassis kit
- A Raspberry Pi compatible camera
- 2 battery packs (For powering the Pi and Motors seperately)
- USB Wireless Adapter
- DC Motor Control Board (2 H-Bridge Circuits) QKits Link 

PiRover employs three software components, implemented in Python2, Python3, and standard POSIX scripts: `PiRover`, the clientside software; `PiServer`, the serverside control software; either of two types of neural network that can be optionally employed by `PiServer` - `tiny-yolo` (implemented in the darkflow framework) and `SENURA'S CNN` (implemented in the tensorflow framework)

## `PiRover`
The `PiRover` software consists of three modules and main.py:
- `cameraStream` interfaces with the camera, used to periodically photograph environment
- `controlStream` interfaces with the motors, used for navigation
- `navigationSystem` controls navigation behaviour, moves randomly until a target is found, and then approaches the target
- `main` interfaces with PiServer, sends photos, parses and receives environmental data, sending control signals to `navigationSystem`

## `PiServer`
`PiServer` interfaces with the `PiRover` over a LAN, forwarding images to either of two CNN models, `tiny-yolo` and `SENURA-CNN`. Each model processes image data asynchronously, and yields JSON indicating the bounding boxes for the scene (if any).

Currently `server.py` and `networkSend.py` need to be linked into the `darkflow` directory and run from there in order for yolo to work

## `SENURA-CNN`
Divide the image into an NxN grid. Pass an image classifier trained on the target object over each grid square. The square with highest activation is designated to contain the target object.
This method will output a coarse bounding box, however the implementation is simple. This method can be optimized by manipulating values of N to find the best grid square-size.

## `tiny-yolo`
`tiny-yolo` is a small variant of the YOLOv2 network, trained on the PascalVOC 2007 tagged image database. YOLO, short for "You Only Look Once", feeds the entire image through a deep, fully-connected, feedforward leaky convolutional neural network, employing global context to make predictions. It achieves high performance by using logistic regression to predict candidate boxes (of predicted boxes, best-candidates are selected through the neural net) and a multilabel training scheme that does not punish overlapping predictions.

The darkflow framework provides a simple interface for designing and training neural networks. Network design and training routine were specified using darkflow cfg syntax.

## Project structure
- The `PiRover` directory contains all scripts to be run on the Raspberry Pi, written in Python 2. The following dependencies are available through pip:
--
-The PiServer direcetory containst all scripts to be run on the server, written in Pythoni 3. The following dependencies are available through pip
- `tiny-yolo` contains the tiny-yolo network and the darkflow framework. Darkflow is not actively maintained and requires specific dependencies best installed in a virtual environment. The provided script `setup.sh` installs and configures the environment.
