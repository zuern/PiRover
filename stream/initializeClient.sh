#!/bin/sh
ssh pi@192.168.0.2 'echo "rootpass" | sudo -Sv && bash -s' < python client.py
