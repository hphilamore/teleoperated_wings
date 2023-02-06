
# Programs to run on computer : Motion tracking of hands in a video feed 
**Computer set up and installation:**
Clone git repository: https://github.com/hphilamore/mediapipe_hands_vid_send
Create virtual environment inside cloned repository: Run:[`python3 venv env`]
Add virtual environment to .gitignore file. Run:[`nano .gitignore`] and add line [`/env`]
Activate virtual environment: Run:[`source env/bin/activate`]
pip3 install -r requirements.txt

**Hand tracking test programs**
Demonstrates hand tracking on video feed from default web-cam
Activate virtual environment: Run:[`source env/bin/activate`]
Run:[`python3 hands_tracking_demo.py`]
 
Demonstrates hand tracking on video feed from default web-cam and outputs coordinates of hand nodes
Activate virtual environment: Run:[`source env/bin/activate`]
Run:[`python3 hands_tracking_demo_coordinates.py`]

**Teleoperation programs**
Tracks hand position in image from web-cam. 
Chooses a command based on hand position.
Sends command to raspberry pi robot over wifi. 
Activate virtual environment: Run:[`source env/bin/activate`]
Run:[`python3 telepresence-client.py`]

Tracks hand position in image from web-cam OR desktop window
Chooses a command based on hand position.
Sends command to raspberry pi robot over wifi. 
Activate virtual environment: Run:[`source env/bin/activate`]
Run `telepresence-server.py` on robot to listen for client. 
Run:[`python3 telepresence-client-win.py`]
Note: Variable `HOST` should have same value equal to raspberry pi IP address
Note: Variable `PORT` should have same value as in [`telepresence-server.py`] 

# Programs to run on robot : Moving in resopnse to commands sent from computer  

**Raspberry pi set up and installation:**
Install buster legacy lite OS 
Add any additional wrifi networks to etc/wpa_supplicant/wpa_supplicant.conf

(Optional) add static IP. Add following snippet to /etc/dhcpcd.conf:

	`
	interface wlan0
	static ip_address=192.168.11.13 #(desired IP)
	static routers=192.168.11.1 #(router IP)
	`

Open a terminal. Run:[`sudo raspi-config`]. Enable all interfaces (serial, camera, remote GPIO)
Run:[`sudo apt update`]
Run:[`sudo apt install git`]
Run:[`sudo apt-get install python3-pip`]
Run:[`sudo apt-get install python3-venv`]
Clone git repository: https://github.com/hphilamore/teleoperated_turtle_robot.git
Create virtual environment inside cloned repository: Run:[`python3 -m venv env`]
Add virtual environment to .gitignore file. Run:[`nano .gitignore`] and add line [`/env`]
Activate virtual environment: Run:[`source env/bin/activate`]
Run:[`pip3 install -r requirements.txt`]
Run: [`pip3 install gpiozero rpi-gpio`]


**Motor test program**
Robot spins motors to tst they are working
Activate virtual environment: Run:[`source env/bin/activate`]
Run:[`python3 motor_test.py`] 

**Telepresence program:**
Robot reposnds to commands sent from computer 
Activate virtual environment: Run:[`source env/bin/activate`]
Run:[`python3 telepresence-server.py`] 
Note: Variable `PORT` should have same value as in [`telepresence-client.py`] / [`telepresence-client-win.py`] 



If you see this warning when using ssh:
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Enter this:
ssh-keygen -R <IP_address>
