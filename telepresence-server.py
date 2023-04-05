#!/usr/bin/env python3

import socket
# from gpiozero import Motor, OutputDevice
from time import sleep
from time import time
import RPi.GPIO as GPIO
import serial
#import time
import os
from py_ax12 import *

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)     # Control Data Direction Pin
GPIO.setup(6,GPIO.OUT)      
GPIO.setup(26,GPIO.OUT)

# right = 0x01
# left = 0x02

# Define and setup GPIO pins
# Rigth foot
# motor1 = Motor(24, 27)
# motor1_enable = OutputDevice(5, initial_value=1)
# # Left foot
# motor2 = Motor(6, 22)
# motor2_enable = OutputDevice(17, initial_value=1)
# # Right tentacle
# motor3 = Motor(23, 16)
# motor3_enable = OutputDevice(12, initial_value=1)
# # Left tentacle
# motor4 = Motor(13, 18)
# motor4_enable = OutputDevice(25, initial_value=1) 

# HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 65443  # Port to listen on (non-privileged ports are > 1023)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

time_old = time()
flag_wings = True

# Create serial object 
Dynamixel=serial.Serial("/dev/serial0",baudrate=1000000,timeout=0.1, bytesize=8)   # UART in ttyS0 @ 1Mbps

while(1):

    conn, addr = server_socket.accept()
    with conn:
        print(f"Connected by {addr}")

        while True:

            set_endless(0x03, False, Dynamixel)
            set_endless(0x04, False, Dynamixel)
            set_endless(0x02, False, Dynamixel)
            set_endless(0x01, False, Dynamixel)
            GPIO.output(18,GPIO.HIGH)

            data = conn.recv(1024)
            if not data:
                break
            msg = data.decode()
            print(msg)

            if msg == 'stop':
                pass
                # set_endless(0x03, False, Dynamixel)
                # set_endless(0x04, False, Dynamixel)

                # GPIO.output(18,GPIO.HIGH)
                # move(0x04, 0, Dynamixel)
                # move(0x03, 0, Dynamixel)
                # move(0x02, 0, Dynamixel)
                # move(0x01, 0, Dynamixel)
                # sleep(1)
                # move(0x04, 150, Dynamixel)
                # move(0x03, 150, Dynamixel)
                # move(0x02, 150, Dynamixel)
                # move(0x01, 150, Dynamixel)
                # sleep(1)

            elif msg == 'left':
                move(0x04, 0, Dynamixel)
                move(0x03, 0, Dynamixel)
                move(0x02, 0, Dynamixel)
                move(0x01, 0, Dynamixel)
                sleep(0.1)

            elif msg == 'right':
                move(0x04, 150, Dynamixel)
                move(0x03, 150, Dynamixel)
                move(0x02, 150, Dynamixel)
                move(0x01, 150, Dynamixel)
                sleep(0.1)
                

            elif msg == 'forward':
                pass

            #conn.sendall(data)
    


