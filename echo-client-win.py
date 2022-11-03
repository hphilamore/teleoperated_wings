#!/usr/bin/env python3
# https://realpython.com/python-sockets/

import socket
import cv2
import mediapipe
import socket
import pyautogui
import numpy as np
from PIL import ImageGrab
from mss import mss
from subprocess import Popen, PIPE
import time
 
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

# TODO: Variables as command line arguments

# Set up server ID and port 
# HOST = "192.168.227.193"    # The raspberry pi's hostname or IP address
HOST = "192.168.128.12"    # The raspberry pi's hostname or IP address
PORT = 65442                # The port used by the server

input_mode = 'window'       # 'camera' / 'window'

# Window name is using window
win_name = 'zoom.us'                      # Temp fix
#win_name = 'Microsoft Teams'
win_name = 'zoom.us:Zoom Meeting'                 # Find zoom meeting window 
#win_name = 'zoom.us:zoom floating video'  # Find zoom meeting window during share screen 
#win_name = 'Vysor'                        # Find vysor window for robot POV 
#win_name = 'Vysor:SM'                        # Find vysor window for robot POV 
#win_name = 'Vysor:ART'                        # Find vysor window for robot POV 

flag_no_hand = False 



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


if input_mode == 'window':
    """
    Set up window to take frame from 

    """ 
    process = Popen(['./windowlist', 'windowlist.m'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    window_positions = stdout.decode().split('\n')

    for w in window_positions:
        if win_name in w:                        # Find vysor window for robot POV
            print(w)
            w = w.split(':')                     # Separate window info 
            print(w)
            coordinates = w[-1].split(',')       # Separate window coordinates
            print(coordinates)
            coordinates = [int(float(i)) for i in coordinates]  # Convert coordinates to integer
            print(coordinates)


while(True):

    with handsModule.Hands(static_image_mode=False, 
                       min_detection_confidence=0.7, 
                       min_tracking_confidence=0.7, 
                       max_num_hands=1) as hands:

        with mss() as sct:
            # Use coordinates of window
            if input_mode == 'window':
                monitor = {"top": coordinates[1], 
                           "left": coordinates[0], 
                           "width": coordinates[3], 
                           "height": coordinates[2]
                           }
                # monitor = {"top": 0, 
                #            "left": 0, 
                #            "width": 500, 
                #            "height": 500
                #            }

            
            # Grab current image            
            if input_mode == 'window':
                """
                Input taken from window
                """
                frame = np.array(sct.grab(monitor))
                frame = np.array(ImageGrab.grab())                # include this line if full screen image required
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            else:
                """
                Input taken from webcam
                """
                ret, frame = capture.read()
                #frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.flip(frame, 1)

            results = hands.process(frame)

            # Check if hand detected
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

                    # Choose a command to send to server socket on raspberry pi 
                    command = pos_to_command(x, z)
                    print(command)

                # # Send command to server socket on raspberry pi        
                # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                #     #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow reuse of address
                #     s.connect((HOST, PORT))
                #     s.sendall(command.encode())

            else:
                print('No hand')
                if not flag_no_hand:     # If there was a hand in previous frame
                    flag_no_hand = True  # Raise the flag 
                    start = time.time()  # Start the timer
                    command = 'no command'

                else:
                    end = time.time()
                    if end-start >= 3:
                        flag_no_hand = False  # Lower the flag 
                        print('stop')
                        command = 'stop'  



            # # Send command to server socket on raspberry pi        
            # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            #     #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow reuse of address
            #     s.connect((HOST, PORT))
            #     s.sendall(command.encode()) 






            try:
                cv2.namedWindow('image',cv2.WINDOW_NORMAL) # Implicitly create the window
                cv2.resizeWindow('image', 590,384)         # Resize the window
                cv2.imshow('image', frame)                 # Show the window 
            except:
                pass
     
            if cv2.waitKey(1) == 27:
                break
