#!/bin/sh
# Run this script locally on the server to initialize and set everything up for operation

echo "Spawning server process locally"
bash initializeServer.sh &

echo "Spawning client process on PiRover"
bash initializeClient.sh & 
