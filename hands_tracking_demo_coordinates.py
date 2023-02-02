import cv2
import mediapipe
import socket
 
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

HOST = "192.168.0.101"  # The raspberry pi's hostname or IP address
PORT = 65432  # The port used by the server

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

    #print(out)
    return out
 
capture = cv2.VideoCapture(0)
 
with handsModule.Hands(static_image_mode=False, 
                       min_detection_confidence=0.7, 
                       min_tracking_confidence=0.7, 
                       max_num_hands=2) as hands:
 
    while (True):
 
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

 
        cv2.imshow('Test hand', frame)
 
        if cv2.waitKey(1) == 27:
            break
 
cv2.destroyAllWindows()
capture.release()