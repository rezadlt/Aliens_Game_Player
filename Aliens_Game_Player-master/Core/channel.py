import RPi.GPIO as GPIO
import time
import requests


channel = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)


def callback(channel):
	if GPIO.input(channel): print("Sound Detected!"); requests.get("http://192.168.1.130:5000/shoot") 
	else: print("Sound Detected!"); requests.get("http://192.168.1.130:5000/shoot") 


GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(channel, callback)


while True:
	time.sleep(1)
    