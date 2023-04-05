#!/usr/bin/env python3

"""

TODO:
- servo should read current positions and not do a full rotation when returning to start position
- Close port if program crashes so that new number doesn’t have to be used 
- GPIO all pins to zero when program killed (e.g. no motors left spinning)
    - https://raspi.tv/2013/rpi-gpio-basics-3-how-to-exit-gpio-programs-cleanly-avoid-warnings-and-protect-your-pi
    - https://gpiozero.readthedocs.io/en/stable/migrating_from_rpigpio.html

"""

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
    


