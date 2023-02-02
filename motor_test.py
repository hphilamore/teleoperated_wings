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


try:

	# Full speed feet forwards
	motor1.forward()
	motor2.forward()
	sleep(1)


	for i in range(3):
		# Full speed tentacles forwards
		motor3.forward()
		motor4.forward()

		sleep(3)

		# motor3.backward()
		# motor4.backward()

		# sleep(3)

		# Tentacles off
		motor3.stop()
		motor4.stop()

		sleep(4)

	motor1.stop()
	motor2.stop()

except KeyboardInterrupt:
    # Code to run before the program exits when you press CTRL+C
    print('exiting...') # print value of counter

# except:
#     # this catches ALL other exceptions including errors.
#     # You won't get any error messages for debugging
#     # so only use it once your code is working
#     print "Other error or exception occurred!"


# finally:
#     GPIO.cleanup() # this ensures a clean exit