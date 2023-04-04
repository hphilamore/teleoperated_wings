import RPi.GPIO as GPIO
import serial
# import time
import os
from time import sleep
from time import time
from py_ax12 import *

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)     # Control Data Direction Pin
GPIO.setup(6,GPIO.OUT)      
GPIO.setup(26,GPIO.OUT)

# right = 0x01
# left = 0x02

# Create serial object 
Dynamixel=serial.Serial("/dev/serial0",baudrate=1000000,timeout=0.1, bytesize=8)   # UART in ttyS0 @ 1Mbps

 

# # Hex values to appear in instruction packet sent to servo
# ax_start = 0xFF       # 2 x FF bytes indicate start of incoming packet 
# ax_id = 0x01          # servo ID 
# ax_goal_length = 0x05 # length of instruction packet (N parameters + 2)

# # instructions for servo to perform 
# ax_ping = 0x01
# ax_read_data = 0x02
# ax_write_data = 0x03
# ax_reg_write = 0x04
# ax_action = 0x05
# ax_reset = 0x06
# ax_sync_write = 0x83
# ax_ccw_angle_limit_l = 0x08
# ax_ccw_al_lt = 0x00
# ax_ccw_al_l = 0xFF
# ax_ccw_al_h = 0x03
# ax_speed_length = 0x05
# ax_goal_speed_l = 0x20
# ccw = 0
# cw = 1


# def move(servo_id, position):

# 	P = position  # position as 10-bit number
	
# 	print(P/1024 * 300)

# 	h = P >> 8    # value of high 8 bit byte

# 	l = P & 0xff  # value of low 8-bit byte                 
	
# 	checksum = ~(servo_id + ax_goal_length + ax_write_data + 0x1E + h + l) & 0xff

#   # convert to hex number full representation (with 0x...) 
# 	checksum = format(checksum, '#04x') 
	
# 	instruction_packet = (format(ax_start, '02x') + " " +
#                           format(ax_start, '02x') + " " +
#                           format(servo_id, '02x') + " " + 
#                           format(ax_goal_length, '02x') + " " +
#                           format(ax_write_data, '02x') + " " +
#                           format(0x1E, '02x') + " " +
#                           format(l, '02x') + " " +
#                           format(h, '02x') + " " +
#                           checksum[2:] 
#                           ).upper()
#                           #str(ax_write_data) + str(0x1E) + str(l) + str(h) + str(checksum))
	
# 	#print(instruction_packet)
	
# 	Dynamixel.write(bytearray.fromhex(instruction_packet))

# 	return(instruction_packet)



# def set_endless(servo_id, status):
    
#     if status: # turn endless rotation on               
	
#         checksum = ~(servo_id + ax_goal_length + ax_write_data + ax_ccw_angle_limit_l) & 0xff
#         checksum = format(checksum, '#04x') # convert to hex number full representation (with 0x...) 
        
#         #print('checksum = ', checksum)
        
#         instruction_packet = (format(ax_start, '02x') + " " +
#                               format(ax_start, '02x') + " " +
#                               format(servo_id, '02x') + " " + 
#                               format(ax_goal_length, '02x') + " " +
#                               format(ax_write_data, '02x') + " " +
#                               format(ax_ccw_angle_limit_l, '02x') + " " +
#                               format(ax_ccw_al_lt, '02x') + " " +
#                               format(ax_ccw_al_lt, '02x') + " " +
#                               checksum[2:] 
#                                ).upper()
                              
	
#     else: # turn endless rotation off
        
#         checksum = ~(servo_id + ax_goal_length + ax_write_data +
#                      ax_ccw_angle_limit_l + ax_ccw_al_l + ax_ccw_al_h) & 0xff
#         checksum = format(checksum, '#04x') # convert to hex number full representation (with 0x...)
        
#         print('checksum = ', checksum)
        
#         instruction_packet = (format(ax_start, '02x') + " " +
#                               format(ax_start, '02x') + " " +
#                               format(servo_id, '02x') + " " + 
#                               format(ax_goal_length, '02x') + " " +
#                               format(ax_write_data, '02x') + " " +
#                               format(ax_ccw_angle_limit_l, '02x') + " " +
#                               format(ax_ccw_al_l, '02x') + " " +
#                               format(ax_ccw_al_h, '02x') + " " +
#                               checksum[2:] 
#                               ).upper()
        
#     #print(instruction_packet)
    
#     Dynamixel.write(bytearray.fromhex(instruction_packet))
    
#     return(instruction_packet)



# def turn(servo_id, side, speed):
#     if side == ccw:
#         #print('ccw')
#         speed_h = speed >> 8 # convert position as 10-bit number to high 8 bit byte
#         speed_l = speed & 0xff
        
#     else:
#         #print('cw')
#         speed_h = (speed >> 8) + 4
#         speed_l = speed & 0xff
        
#     checksum = ~(servo_id + ax_speed_length + ax_write_data +
#                  ax_goal_speed_l + speed_l + speed_h) & 0xff
    
#     checksum = format(checksum, '#04x') # convert to hex number full representation (with 0x...)
    
#     #print('checksum = ', checksum)
    
#     instruction_packet = (format(ax_start, '02x') + " " +
#                           format(ax_start, '02x') + " " +
#                           format(servo_id, '02x') + " " + 
#                           format(ax_speed_length, '02x') + " " +
#                           format(ax_write_data, '02x') + " " +
#                           format(ax_goal_speed_l, '02x') + " " +
#                           format(speed_l, '02x') + " " +
#                           format(speed_h, '02x') + " " +
#                           checksum[2:] 
#                           ).upper()
        
#     #print(instruction_packet)
    
#     Dynamixel.write(bytearray.fromhex(instruction_packet))
    
#     return(instruction_packet)


# def sweep(servo_id):
#     for i in range(300):
#         move(servo_id, int(i/300 * 1024))
#         time.sleep(0.1)
#         print(i)
        
# def binary_position(servo_id, x):
#     set_endless(servo_id, False)
#     if x > 0.5:
#         GPIO.output(18,GPIO.HIGH) 
#         angle = 0
#         move(servo_id, int(angle/300 * 1024))
#         print(angle)

        
#     else:
#         GPIO.output(18,GPIO.HIGH)
#         angle = 60
#         move(servo_id, int(angle/300 * 1024))   
#         print(angle)


# def binary_rotation(servo_id, x):
#     set_endless(servo_id, True)
#     if x > 0.5:
#         GPIO.output(18,GPIO.HIGH) 
#         turn(servo_id, ccw, 500)


#     else:
#         GPIO.output(18,GPIO.HIGH)
#         turn(servo_id, cw, 500)
        
        
        
# def follow_hand(x, z):
#     GPIO.output(18,GPIO.HIGH) 
#     set_endless(0x01, True)
#     set_endless(0x02, True)
    
#     if 0.0 < x < 1.0:              # hand detected in frame
#         #val = int(255 * x)
#         z_scale_factor = 10; 
#         val = int(255 * z_scale_factor * abs(z))
#         if val>255:val=255         # cap value sent over i2c at 255  
#         print(val);
        
#         if z <= -0.15:
#             print('stop')
#             turn(left, ccw, 0)
#             turn(right, cw, 0)
        
#         elif x < 0.4:                # turn left
#             print('hand left')
#             move(0x03, 300)
#             time.sleep(0.4)
#             move(0x03, 0)
#             #turn(left, ccw, 500)
#             #turn(right, cw,  0)
             
#         elif x > 0.6:              # turn right
#             print('hand right')
#             move(0x04, 300)
#             time.sleep(0.4)
#             move(0x04, 0)
#             #turn(left, ccw,  0)
#             #turn(right, cw, 500)
            
#         else:                      # go forwards
#             print('hand centre')
#             turn(right, cw,  500)
#             turn(left, ccw, 500)
            
            
        
# def continuous_position(servo_id, x):
#     #  Continous position selection based on hand tracking
#     if x >= 0:                         # move function only accepts positive integers 
#         finger_x_pos = x
#         finger_x_pos *= 1024
#         move(servo_id, int(finger_x_pos)) 


# def binary_scribbler_GPIO(x):

#     if x > 0.5:
#         GPIO.output(6,GPIO.HIGH) 
#         GPIO.output(26,GPIO.LOW) 
#         angle = 0
#         print(angle)

        
#     else:
#         GPIO.output(26,GPIO.HIGH) 
#         GPIO.output(6,GPIO.LOW)  
#         angle = 60
#         print(angle)
        
        
# def forwards():
#     GPIO.output(18,GPIO.HIGH) 
#     set_endless(left, True)
#     set_endless(right, True)
    
#     turn(left, ccw,1000)
#     turn(right, cw, 1000)    


# def move_check(servo_id, position):

# 	P = position  # position as 10-bit number 

# 	B = P/256               # seperate into 2 8 bit bytes by dividing by max value of 8 bit byte 

# 	H = int(B // 1)         # decimal value of high byte, convert to intager

# 	L = B - H                     
# 	L = int(L * 256)        # decimal value of low byte

# 	H = hex(H)

# 	L = hex(L)
	
# 	print(H,L)

# 	return(H, L)

 
set_endless(0x03, False, Dynamixel)
set_endless(0x04, False, Dynamixel)

while True:

  GPIO.output(18,GPIO.HIGH)
  move(0x04, 0, Dynamixel)       
  sleep(1)
  move(0x04, 150, Dynamixel)
  sleep(1)
