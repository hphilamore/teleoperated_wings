#!/usr/bin/env python3

import socket
from gpiozero import Motor, OutputDevice
from time import sleep

# Define and setup GPIO pins
# Left foot
motor1 = Motor(24, 27)
motor1_enable = OutputDevice(5, initial_value=1)
# Right foot
motor2 = Motor(6, 22)
motor2_enable = OutputDevice(17, initial_value=1)
# Right tentacle
motor3 = Motor(23, 16)
motor3_enable = OutputDevice(12, initial_value=1)
# Left tentacle
motor4 = Motor(13, 18)
motor4_enable = OutputDevice(25, initial_value=1) 

# HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 65436  # Port to listen on (non-privileged ports are > 1023)

while(1):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow reuse of address
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                msg = data.decode()
                print(msg)

                if msg == 'stop':
                    motor1.stop()
                    motor2.stop()

                elif msg == 'left':
                    motor1.forward(0.5)
                    motor2.stop()

                elif msg == 'right':
                    motor1.stop()
                    motor2.forward(0.5)

                elif msg == 'forward':
                    motor1.forward(0.5)
                    motor2.forward(0.5)

                conn.sendall(data)
