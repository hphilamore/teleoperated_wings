#!/usr/bin/env python3

import socket
# from gpiozero import Motor, OutputDevice
from time import sleep
from time import time
import RPi.GPIO as GPIO
import serial
#import time
import os

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)     # Control Data Direction Pin
GPIO.setup(6,GPIO.OUT)      
GPIO.setup(26,GPIO.OUT)

right = 0x01
left = 0x02

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
PORT = 65442  # Port to listen on (non-privileged ports are > 1023)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

time_old = time()
flag_wings = True

# Create serial object 
Dynamixel=serial.Serial("/dev/serial0",baudrate=1000000,timeout=0.1, bytesize=8)   # UART in ttyS0 @ 1Mbps

 

# Hex values to appear in instruction packet sent to servo
ax_start = 0xFF       # 2 x FF bytes indicate start of incoming packet 
ax_id = 0x01          # servo ID 
ax_goal_length = 0x05 # length of instruction packet (N parameters + 2)

# instructions for servo to perform 
ax_ping = 0x01
ax_read_data = 0x02
ax_write_data = 0x03
ax_reg_write = 0x04
ax_action = 0x05
ax_reset = 0x06
ax_sync_write = 0x83
ax_ccw_angle_limit_l = 0x08
ax_ccw_al_lt = 0x00
ax_ccw_al_l = 0xFF
ax_ccw_al_h = 0x03
ax_speed_length = 0x05
ax_goal_speed_l = 0x20
ccw = 0
cw = 1


def move(servo_id, position):

    P = position  # position as 10-bit number
    
    print(P/1024 * 300)

    h = P >> 8    # value of high 8 bit byte

    l = P & 0xff  # value of low 8-bit byte                 
    
    checksum = ~(servo_id + ax_goal_length + ax_write_data + 0x1E + h + l) & 0xff

  # convert to hex number full representation (with 0x...) 
    checksum = format(checksum, '#04x') 
    
    instruction_packet = (format(ax_start, '02x') + " " +
                          format(ax_start, '02x') + " " +
                          format(servo_id, '02x') + " " + 
                          format(ax_goal_length, '02x') + " " +
                          format(ax_write_data, '02x') + " " +
                          format(0x1E, '02x') + " " +
                          format(l, '02x') + " " +
                          format(h, '02x') + " " +
                          checksum[2:] 
                          ).upper()
                          #str(ax_write_data) + str(0x1E) + str(l) + str(h) + str(checksum))
    
    #print(instruction_packet)
    
    Dynamixel.write(bytearray.fromhex(instruction_packet))

    return(instruction_packet)



def set_endless(servo_id, status):
    
    if status: # turn endless rotation on               
    
        checksum = ~(servo_id + ax_goal_length + ax_write_data + ax_ccw_angle_limit_l) & 0xff
        checksum = format(checksum, '#04x') # convert to hex number full representation (with 0x...) 
        
        #print('checksum = ', checksum)
        
        instruction_packet = (format(ax_start, '02x') + " " +
                              format(ax_start, '02x') + " " +
                              format(servo_id, '02x') + " " + 
                              format(ax_goal_length, '02x') + " " +
                              format(ax_write_data, '02x') + " " +
                              format(ax_ccw_angle_limit_l, '02x') + " " +
                              format(ax_ccw_al_lt, '02x') + " " +
                              format(ax_ccw_al_lt, '02x') + " " +
                              checksum[2:] 
                               ).upper()
                              
    
    else: # turn endless rotation off
        
        checksum = ~(servo_id + ax_goal_length + ax_write_data +
                     ax_ccw_angle_limit_l + ax_ccw_al_l + ax_ccw_al_h) & 0xff
        checksum = format(checksum, '#04x') # convert to hex number full representation (with 0x...)
        
        print('checksum = ', checksum)
        
        instruction_packet = (format(ax_start, '02x') + " " +
                              format(ax_start, '02x') + " " +
                              format(servo_id, '02x') + " " + 
                              format(ax_goal_length, '02x') + " " +
                              format(ax_write_data, '02x') + " " +
                              format(ax_ccw_angle_limit_l, '02x') + " " +
                              format(ax_ccw_al_l, '02x') + " " +
                              format(ax_ccw_al_h, '02x') + " " +
                              checksum[2:] 
                              ).upper()
        
    #print(instruction_packet)
    
    Dynamixel.write(bytearray.fromhex(instruction_packet))
    
    return(instruction_packet)



while(1):
    # #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow reuse of address
    #     # s.bind((HOST, PORT))
    #     # s.listen()
    # #try:

    # # Switch wing direction every 3s
    # time_new = time()
    # if time_new-time_old >= 3:
    #     flag_wings = not flag_wings
    #     time_old = time_new
    #     print('switched wing direction')

    # # Switch wings on/off
    # if flag_wings:
    #     print('wings up')
    #     motor3.forward()
    #     motor4.forward()
    # else:
    #     print('wings down')
    #     motor3.stop()
    #     motor4.stop()

    # print('looper')



    conn, addr = server_socket.accept()
    with conn:
        print(f"Connected by {addr}")



        while True:

            # time_new = time()
            # if time_new-time_old >= 2:
            #     flag_wings = not flag_wings
            #     time_old = time_new
            #     print('switched wing direction')
            #     #sleep(2)

            # # # Switch wings on/off
            #     if flag_wings:
            #         print('wings up')
            #         motor3.forward()
            #         motor4.forward()
            #     else:
            #         print('wings down')
            #         motor3.stop()
            #         motor4.stop()




            data = conn.recv(1024)
            if not data:
                break
            msg = data.decode()
            print(msg)

            if msg == 'stop':
                set_endless(0x03, False)
                set_endless(0x04, False)
                
                GPIO.output(18,GPIO.HIGH)
                move(0x04, 0)
                time.sleep(1)
                move(0x04, 150)
                time.sleep(1)
            #     motor1.stop() 
            #     motor2.stop()
            #     motor3.stop() 
            #     motor4.stop()

            # elif msg == 'left':
            #     motor1.stop()
            #     motor2.forward(0.5)

            # elif msg == 'right':
            #     motor1.forward(0.5)
            #     motor2.stop()
                

            # elif msg == 'forward':
            #     motor1.forward(0.5)
            #     motor2.forward(0.5)

            #conn.sendall(data)
    
    # except:
    #     print('no comms')


# except KeyboardInterrupt:
#         pass

