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
import numpy as np
import RPi.GPIO as GPIO
import serial
import os
from py_ax12 import *


# Setup GPIO pins 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)     # Control Data Direction Pin
GPIO.setup(6,GPIO.OUT)      
GPIO.setup(26,GPIO.OUT)


# HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 65443      # Port to listen on (non-privileged ports are > 1023)


# Setup raspberry pi as server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

# Create serial object 
Dynamixel=serial.Serial("/dev/serial0",baudrate=1000000,timeout=0.1, bytesize=8)   # UART in ttyS0 @ 1Mbps

def running_mean(new_val, arr, win_size):
    arr.insert(0, new_val)
    arr = arr[:win_size]
    print(arr)
    return np.nanmean(np.array(arr[:win_size]))


arr_left = list(np.full((5,), np.nan))
arr_right = list(np.full((5,), np.nan))

hand_left = False
hand_right = False


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
            # print(msg)

            if msg != 'no command' and msg != 'stop':

                coordinates = msg.split(',')

                # Convert string to floating point data 
                coordinates = [float(i) for i in coordinates]

                # Grouped coordintes in x,y pairs for each hand detected
                hands = [coordinates[i:i+2] for i in range(0, len(coordinates), 2)]

                # print(coordinates)

                # If 2 hands detected:
                if len(hands) > 1:

                    # If x coordinate of both hands are on the same side of the screen, ignore one hand
                    if ((hands[0][0]<0.5 and hands[1][0]<0.5) or
                        (hands[0][0]>=0.5 and hands[1][0]>=0.5)):
                        hands = [hands[0]]

                # For each hand 
                for i in hands:

                    x_position = i[0]
                    y_position = i[1] 

                    # convert to 10-bit value
                    servo_position = (y_position * 1024) 

                    # Cap all negative values at 0
                    if servo_position<1: servo_position = 0 

                    # Convert floating point to integer
                    servo_position = int(servo_position)

                    # Hand x position on left side of screen
                    if x_position<0.5:

                        # hand_left = True

                        # Moving average filter applied, Position rounded to nearest decimal value
                        smoothed_position = int(running_mean(servo_position, arr_left, 20)) //10 * 10

                        # Send 10-bit value to servo
                        # move(0x04, servo_position, Dynamixel)
                        move(0x04, smoothed_position, Dynamixel)

                    # else:
                        # hand_left = False


                    # Hand x position on right side of screen
                    if x_position>=0.5:

                        # hand_right = True

                        # Moving average filter applied, Position rounded to nearest decimal value
                        smoothed_position = int(running_mean(servo_position, arr_right, 20)) //10 * 10


                        # Send 10-bit value to servo
                        # move(0x03, servo_position, Dynamixel)
                        move(0x03, smoothed_position, Dynamixel)

                    # else:
                    #     hand_right = False



            #     # Reset filter array if no hand detected on right or left 
            #     if not hand_left:
            #         arr_left = list(np.full((5,), np.nan))

            #     if not hand_right:
            #         arr_right = list(np.full((5,), np.nan))

            # # Reset filter array if no hand detected on right and left 
            # else:
            #     arr_left = list(np.full((5,), np.nan))
            #     arr_right = list(np.full((5,), np.nan))














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
    


