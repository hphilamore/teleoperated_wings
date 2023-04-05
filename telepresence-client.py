#!/usr/bin/env python3

"""
#----------------------------------------------------------

Tracks hand position in image from web-cam. 

Chooses a command based on hand position.

Sends command to raspberry pi robot over wifi. 

https://realpython.com/python-sockets/

#----------------------------------------------------------
"""


import socket
import cv2
import mediapipe
import socket
import time
 
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

HOST = "192.168.134.93"  # The raspberry pi's hostname or IP address
PORT = 65443            # The port used by the server

flag_no_hand = False 

# Setup web cam ready for video capture 
capture = cv2.VideoCapture(0)

def pos_to_command(x, z):
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
 

while(True):

    with handsModule.Hands(static_image_mode=False, 
                       min_detection_confidence=0.7, 
                       min_tracking_confidence=0.7, 
                       max_num_hands=2) as hands:

        # Capture image from video
        ret, frame = capture.read()
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

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
 
                x_ = []
                z_ = []

                for i in range(20):
                    x_.append(hand_landmarks.landmark[handsModule.HandLandmark(i).value].x)
                    z_.append(hand_landmarks.landmark[handsModule.HandLandmark(i).value].z)
                        
                # Find mean value of x and z coordinate of nodes 
                x = sum(x_)/len(x_)                
                z = sum(z_)/len(z_)

                print(x, z)

                # Choose a command to send to the raspberry pi robot 
                command = pos_to_command(x, z)
                print(command)

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


        # Send command to server socket on raspberry pi
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow reuse of address
            s.connect((HOST, PORT))
            s.sendall(command.encode())
            # data = s.recv(1024)


        try:
            cv2.imshow('Test hand', frame)
        except:
            pass
 
        if cv2.waitKey(1) == 27:
            break
