# PiRover
![PiRover Image](https://github.com/zuern/PiRover/raw/master/Images/PiRover%2001.jpg)

PiRover is a small robot built using electronic components from QKits Kingston. It's purpose is to randomly move through its environment until it identifies a target object, then drive towards the target object. The robot uses object detection via a convolutional neural network to identify the target in the environment (a toy car) and drive towards it. The robot consists of:
- A Raspberry Pi Model B
- A robot chassis kit (Metal Frame + 2 DC Motors)
- A Raspberry Pi compatible camera (PiCamera)
- Two 4xAA battery packs (For powering the Pi and Motors separately)
- USB Wireless Adapter
- DC Motor Control Board (2 H-Bridge Circuits)

PiRover employs three software components, implemented in Python2, Python3: `PiRover`, the clientside software; `PiServer`, the serverside control software; either of two types of neural network that can be optionally employed by `PiServer` - `tiny-yolo` (implemented in the darkflow framework) and `SENURA'S CNN` (implemented in the tensorflow framework).

## `PiRover`
The `PiRover` software consists of three modules and main.py:
- `cameraStream` interfaces with the camera, used to periodically photograph environment and send these photos to the server
- `controlStream` interfaces with the motors, used for converting bounding box information from the server into navigation instructions for `navigationSystem`
- `navigationSystem` handles rover navigation by controlling the DC motors on the chassis using [Pulse Width Modulation](https://en.wikipedia.org/wiki/Pulse-width_modulation)
- `main` is the entry point for the PiRover software, initializing all the other modules 

## `PiServer`
`PiServer` interfaces with the `PiRover` over a LAN, forwarding images to either of two CNN models, `tiny-yolo` and `SENURA-CNN`. Each model processes image data asynchronously, and yields JSON indicating the bounding boxes for the scene (if any).

Currently `server.py` and `networkSend.py` need to be linked into the `darkflow` directory and run from there in order for yolo to work

`main` is the starting point of the server-side code. The code operates by listening for an incoming image from the PiRover. When it recieves the image it saves it to disk, to a folder the CNN is watching.

The CNN will see a new file and process the file, outputting a JSON file containing an array of all the bounding boxes for detected objects. The bounding box data looks like:

```
[{ "label": "car", "confidence": 0.87, "topleft": { "x": 145, "y": 256 }, "bottomright": { "x": 200, "y": 300 } }]
```

## `SENURA-CNN`
Divide the image into an NxN grid. Pass an image classifier trained on the target object over each grid square. The square with highest activation is designated to contain the target object.
This method will output a coarse bounding box, however the implementation is simple. This method can be optimized by manipulating values of N to find the best grid square-size.

## `YOLO` Algorithm
Our second method will be using the YOLO (You Only Look Once) algorithm for object detection.  This functions by determining the “best” locations for bounding boxes, and then passing these regions to the classifier. This happens with only one pass through the CNN and is highly performant.

## Project Structure
- The `PiRover` directory contains scripts to be run on the Raspberry Pi. 
-The `PiServer` directory contains all scripts to be run on the server. The following dependencies are available through pip:
- `tiny-yolo` contains the tiny-yolo network and the darkflow framework. Darkflow is not actively maintained and requires specific dependencies best installed in a virtual environment. The provided script `setup.sh` installs and configures the environment.

### Networking
The Rover and server communicate over Wi-Fi. The rover has its USB Wireless Adapter set to run in Access-Point mode, creating a hotspot that the laptop connects to. The 2 devices then communicate using a simple protocol over sockets.

The networking protocol is simple: First the file length gets sent, then the payload. If a length of 0 is sent, the connection gets closed.
