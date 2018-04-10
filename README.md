# PiRover
PiRover is a small robot built using electronic components from QKits Kingston. The robot uses object detection via a convolutional neural network to identify a target in the environment (a toy car) and drive towards it. Until detection, the robot moves randomly about its environment. The robot consists of:
- A Raspberry Pi Model B
- A robot chassis kit (Metal Frame + 2 DC Motors)
- A Raspberry Pi compatible camera
- Two 4xAA battery packs (For powering the Pi and Motors separately)
- USB Wireless Adapter
- DC Motor Control Board (2 H-Bridge Circuits)


![PiRover Image](https://github.com/zuern/PiRover/raw/master/Images/PiRover%2001.jpg)

## `PiRover`
The `PiRover` software consists of three modules and main.py:
- `cameraStream` interfaces with the camera, used to periodically photograph environment and send these photos to the server
- `controlStream` interfaces with the motors, used for converting bounding box information from the server into navigation instructions for `navigationSystem`
- `navigationSystem` handles rover navigation by controlling the DC motors on the chassis using [Pulse Width Modulation](https://en.wikipedia.org/wiki/Pulse-width_modulation)
- `main` is the entry point for the PiRover software, initializing all the other modules 

## `PiServer`
`PiServer` interfaces with the `PiRover` over a LAN, forwarding images to either of two CNN models, `tiny-yolo` and `SENURA-CNN`. Each model processes image data asynchronously, and yields JSON indicating the bounding boxes for the scene (if any).

PiRover employs three software components, implemented in Python2, Python3, and standard POSIX scripts: `PiRover`, the clientside software; `PiServer`, the serverside control software; either of two types of neural network that can be optionally employed by `PiServer` - `tiny-yolo` (implemented in the darkflow framework) and `SENURA'S CNN` (implemented in the tensorflow framework)

## `PiRover`
Currently `server.py` and `networkSend.py` need to be linked into the `darkflow` directory and run from there in order for yolo to work

`server` is the starting point of the server-side code. The code operates by listening for an incoming image from the PiRover. When it recieves the image it saves it to disk, to a folder the CNN is watching.

The CNN will see new image data and process the it, outputting JSON containing an array of all the bounding boxes for detected objects. The bounding box data looks like:

```
[{ "label": "car", "confidence": 0.87, "topleft": { "x": 145, "y": 256 }, "bottomright": { "x": 200, "y": 300 } }]
```

## `SENURA-CNN`
Divide the image into an NxN grid. Pass an image classifier trained on the target object over each grid square. The square with highest activation is designated to contain the target object.
This method will output a coarse bounding box, however the implementation is simple. This method can be optimized by manipulating values of N to find the best grid square-size.

## `yolov2`
`yolov2` is a small variant of the YOLOv2 network, trained on the COCO tagged image database. YOLO, short for "You Only Look Once", feeds the entire image through a deep, fully-connected, feedforward leaky convolutional neural network, employing global context to make predictions. It achieves high performance by using logistic regression to predict candidate boxes (of predicted boxes, best-candidates are selected through the neural net) and a multilabel training scheme that does not punish overlapping predictions.

The darkflow framework provides a simple interface for designing and training neural networks. Network design and training routine were specified using darkflow cfg syntax.

## Project structure
- The `PiRover` directory contains all scripts to be run on the Raspberry Pi, written in Python 2. The following dependencies are available through pip:
--
-The PiServer direcetory containst all scripts to be run on the server, written in Pythoni 3. The following dependencies are available through pip
- `darkflow` contains the YOLOv2 network and the darkflow framework. Darkflow is not actively maintained and requires specific dependencies best installed in a virtual environment. The provided script `setup.sh` installs and configures the environment.

### Networking
The Rover and server communicate over Wi-Fi. The rover has its USB Wireless Adapter set to run in Access-Point mode, creating a hotspot that the laptop connects to. The 2 devices then communicate using a simple protocol over sockets.

The networking protocol is simple: First the file length gets sent, then the payload. If a length of 0 is sent, the connection gets closed.
