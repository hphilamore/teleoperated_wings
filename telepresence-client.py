#!/usr/bin/env python3
# https://realpython.com/python-sockets/
# https://www.explainingcomputers.com/rasp_pi_robotics.html

"""
#----------------------------------------------------------

Tracks hand position in image from web-cam. 

Chooses a command based on hand position.

Sends command to raspberry pi robot over wifi. 

#----------------------------------------------------------
"""


import socket
import cv2
import mediapipe
import socket
import time

from mss import mss
import sys
from subprocess import Popen, PIPE
import numpy as np

import curses

#-------------------------------------------------------------------------------
""" SETUP """

HOST = "192.168.0.100"  # The raspberry pi's hostname or IP address
PORT = 65443            # The port used by the server

# Take video stream from 'camera' or 'window' or 'keys'
input_mode = 'camera'  

# Window name is using window
win_name = 'zoom.us'                      
#win_name = 'Microsoft Teams'
win_name = 'zoom.us:Zoom Meeting'          # Find zoom meeting window 
#win_name = 'zoom.us:zoom floating video'  # Find zoom meeting window during share screen 
#win_name = 'Vysor'                        # Find vysor window for robot POV 
#win_name = 'Vysor:SM'                     # Find vysor window for robot POV 
#win_name = 'Vysor:ART'                    # Find vysor window for robot POV 
win_name = 'Photo Booth:Photo Booth'   


# Choose OC as macOS or windowsOS 
OS = 'macOS' #'windowsOS'

# Video appears full scree if True
make_output_window_fullscreen = True


#-------------------------------------------------------------------------------

if OS == 'windowsOS': 
    from screeninfo import get_monitors # windows only
 
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

flag_no_hand = False 

# Setup web cam ready for video capture 
capture = cv2.VideoCapture(0)


def pos_to_command(x, y, z):
    """
    Translates position of hand detected to command sent to robot
    """
    print(x, y)
    if 0.0 < x < 1.0:        # Check hand detected in frame
        # if z <= -0.15:       # Stop if too close
        #     out = 'stop'          

        if x < 0.4:        # Turn left
            out = 'left'
             
        elif x > 0.6:        # Turn right 
            out = 'right'
            
        else:                # Go forwards
            if y >= 0.5:
                out = 'backward'
            else:
                out = 'forward'

    else:
        out = 'none'

    return out


if input_mode == 'keys':

    screen = curses.initscr()
    curses.noecho() 
    curses.cbreak()
    screen.keypad(True)

    command = 'stop'

    try:

        while(True):
            char = screen.getch()

            # if char == curses.KEY_UP:
            #     print("up")
            #     command = 'forward'
            if char == ord('q'):
                break
            elif char == curses.KEY_UP:
                print("up")
                command = 'forward'
            elif char == curses.KEY_DOWN:
                print("down")
                command = 'backward'
            elif char == curses.KEY_RIGHT:
                print("right")
                command = 'right'
            elif char == curses.KEY_LEFT:
                print("left")
                command = 'left'
            elif char == ord('s'): #10:
                print("stop")
                command = 'stop' 

            # Send command to server socket on raspberry pi
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow reuse of address
                s.connect((HOST, PORT))
                s.sendall(command.encode())
                # data = s.recv(1024)

    except KeyboardInterrupt:
        #Close down curses properly, inc turn echo back on!
        curses.nocbreak(); screen.keypad(0); curses.echo()
        curses.endwin()


elif input_mode == 'window':
    """ Set up window for image capture """
     
    process = Popen(['./windowlist', 'windowlist.m'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    window_positions = stdout.decode().split('\n')

    for w in window_positions:
        if win_name in w:                        # Find window 
            print(w)
            w = w.split(':')                     # Separate window info 
            print(w)
            coordinates = w[-1].split(',')       # Separate window coordinates
            print(coordinates)
            coordinates = [int(float(i)) for i in coordinates]  # Convert coordinates to integer
            print(coordinates)

elif input_mode == 'camera':
    """ Setup web cam ready for video capture """
    capture = cv2.VideoCapture(0)
 

while(True):

    with handsModule.Hands(static_image_mode=False, 
                       min_detection_confidence=0.7, 
                       min_tracking_confidence=0.7, 
                       max_num_hands=1) as hands:


        # with mss() as sct:
            
        """
        Input taken from window
        """
        if input_mode == 'window':

            with mss() as sct:

                try:
                    # Use coordinates of window
                    # with mss() as sct:
                    window = {"top": coordinates[1], 
                          "left": coordinates[0], 
                          "width": coordinates[3], 
                          "height": coordinates[2]
                           }

                    # Grab current image    
                    frame = np.array(sct.grab(window))

                    # ------------------------------------------------
                    # Uncomment this line if full screen image required
                    # frame = np.array(ImageGrab.grab())
                    # ------------------------------------------------  

                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                except:
                    print("No window with specified name")
                    print("Exiting program...")
                    sys.exit(1)
            

        elif input_mode == 'camera':
            """
            Input taken from webcam
            """
            ret, frame = capture.read()
            # Grab current image    
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 1)


        # Look for hands    
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
 
                x_ = []
                y_ = []
                z_ = []

                for i in range(20):
                    x_.append(hand_landmarks.landmark[handsModule.HandLandmark(i).value].x)
                    y_.append(hand_landmarks.landmark[handsModule.HandLandmark(i).value].y)
                    z_.append(hand_landmarks.landmark[handsModule.HandLandmark(i).value].z)
                        
                # Find mean value of x and z coordinate of nodes 
                x = sum(x_)/len(x_)                
                y = sum(y_)/len(y_)                
                z = sum(z_)/len(z_)

                print(x, y, z)

                # Choose a command to send to the raspberry pi robot 
                command = pos_to_command(x, y, z)
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


        if OS == 'windowsOS': 
            if make_output_window_fullscreen:

                # To make output window full screen:
    	        for monitor in get_monitors():
    	         	screen_h = monitor.height
    	         	screen_w = monitor.width
    	        
    	        frame_h, frame_w, _ = frame.shape

    	        scaleWidth = float(screen_w)/float(frame_w)
    	        scaleHeight = float(screen_h)/float(frame_h)

    	        if scaleHeight>scaleWidth:
    	        	imgScale = scaleWidth
    	        else:
    	        	imgScale = scaleHeight

    	        newX,newY = frame_w*imgScale, frame_h*imgScale

    	        cv2.namedWindow('image',cv2.WINDOW_NORMAL)      # Implicitly create the window
    	        cv2.resizeWindow('image', int(newX),int(newY))  # Resize the window


        try:
            cv2.imshow('image', frame)                 # Show the window 
        	
        except:
            pass
 
        if cv2.waitKey(1) == 27:
            break
