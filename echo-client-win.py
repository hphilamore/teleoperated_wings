#!/usr/bin/env python3
# https://realpython.com/python-sockets/

import socket
import cv2
import mediapipe
import socket
import pyautogui
import numpy as np
from PIL import Image#Grab
from mss import mss
from subprocess import Popen, PIPE
 
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

# Set up server ID and port 
HOST = "192.168.227.193"  # The raspberry pi's hostname or IP address
PORT = 65442            # The port used by the server



def pos_to_command(x, z):
    """
    Returns robot command as a string based on hand node coordinates 
    """
    if 0.0 < x < 1.0:        # Check hand detected in frame
        if z <= -0.15:       # Stop if too close
            out = 'stop'          

        elif x < 0.4:        # Turn left
            out = 'left'
             
        elif x > 0.6:        # Turn right 
            out = 'right'
            
        else:                # Go forwards
            out = 'forward'

    else:
        out = 'none'
        return out

    #print(out)
    return out
 


capture = cv2.VideoCapture(0)

#----------------------------------------
"""
Run code to set up window if using window grab (zoom window)
"""

# REGION = (0, 200, 400, 300) # (left_x, top_y, right_x, bottom_y)
#REGION = (700, 200, 800, 400) # (left_x, top_y, right_x, bottom_y)
#REGION = (899.000000,213.000000,44.000000,264.000000) # (left_x, top_y, right_x, bottom_y)
# width, height = pyautogui.size()
# print(width, height)
process = Popen(['./windowlist', 'windowlist.m'], stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()
window_positions = stdout.decode().split('\n')

for w in window_positions:
    #if 'zoom.us' in w:                 # Temp solution
    #if 'zoom.us:Zoom' in w:                 # Find zoom meeting window
    if 'zoom.us:zoom floating video' in w:   # Find zoom meeting window during share screen
    #if 'Vysor' in w:                          # Find vysor window for robot POV
        print(w)
        w = w.split(':')               # Separate window info 
        print(w)
        coordinates = w[-1].split(',')   # Separate window coordinates
        print(coordinates)
        coordniates = [410.000000,679.000000,40.000000,40.000000]
        coordinates = [int(float(i)) for i in coordinates]  # Separate window coordinates
        print(coordinates)

#----------------------------------------


while(True):

    with handsModule.Hands(static_image_mode=False, 
                       min_detection_confidence=0.7, 
                       min_tracking_confidence=0.7, 
                       max_num_hands=1) as hands:

        with mss() as sct:
            # monitor = {"top": 461, "left": 7, "width": 590, "height": 384}
            monitor = {"top": coordinates[1], 
                       "left": coordinates[0], 
                       "width": coordinates[3], 
                       "height": coordinates[2]
                       }
            #--------------------------------------------------
            # CODE TO GET FRAME:
            """
            If using web-cam
            """
            ret, frame = capture.read()

            """
            If using window grab (zoom window)
            """
            # if using window
            #frame = ImageGrab.grab(bbox=REGION) 
            #frame = np.array(frame)
            frame = np.array(sct.grab(monitor))
            #frame = Image.frombytes("RGB", frame.size, frame.bgra, "raw", "BGRX")  # Convert to PIL.Image
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            #--------------------------------------------------
            #results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            results = hands.process(frame)

            # Check for hands
            if results.multi_hand_landmarks != None:

                # Draw hands
                for handLandmarks in results.multi_hand_landmarks:
                    drawingModule.draw_landmarks(frame, 
                                                 handLandmarks, 
                                                 handsModule.HAND_CONNECTIONS)

                # Find each hand up to max number of hands 
                for hand_no, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    print(f'HAND NUMBER: {hand_no+1}')
                    print('-----------------------')
                    # Find mean of x, y position of all nodes  
                    x_ = []
                    z_ = []

                    for i in range(20):
                        x_.append(hand_landmarks.landmark[handsModule.HandLandmark(i).value].x)
                        z_.append(hand_landmarks.landmark[handsModule.HandLandmark(i).value].z)
                            
                    # Find mean value of x and z coordinate of ndodes 
                    x = sum(x_)/len(x_)                
                    z = sum(z_)/len(z_)

                    print(x, z)

                    # Choose a command to send to the raspberry pi 
                    command = pos_to_command(x, z)
                    print(command)

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow reuse of address
                    s.connect((HOST, PORT))
                    #s.sendall(b"Hello, world")
                    s.sendall(command.encode())
                    data = s.recv(1024)

                print(f"Received {data!r}")

            try:
                cv2.namedWindow('image',cv2.WINDOW_NORMAL) # Implicitly create the window
                cv2.resizeWindow('image', 590,384)         # Resize the window
                cv2.imshow('image', frame)                 # Show the window 
            except:
                pass
     
            if cv2.waitKey(1) == 27:
                break
