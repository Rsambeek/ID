import time
import wiringpi
import socket
import docker
import os
import MySQLdb


client = docker.from_env()	# Get current client
node = client.nodes.get(socket.gethostname())   # get current node in docker swarm

labelError = False

try:
    print("Inspectorgadget: ", node.attrs['Spec']['Labels']['inspectorgadget'])
except:
    labelError = True

try:
    print("Gatekeeper: ", node.attrs['Spec']['Labels']['gatekeeper'])
except:
    labelError = True

try:
    print("Gatereader: ", node.attrs['Spec']['Labels']['gatereader'])
except:
    labelError = True

if labelError:
    print("Resetting missing labels")
    node.update({'Availability': 'active', 'Name': socket.gethostname(), 'Role': 'manager', 'Labels': {'inspectorgadget': 'True', 'gatekeeper': 'True', 'gatereader': 'True'}})
    os.system('sudo reboot now')


servoPin1 = 17  #Setup variables for pins for servo's
servoPin2 = 18
servoCheck1 = 29
servoCheck2 = 31
sensorTrigger = 32
sensorEcho = 35
pud = pigpio.PUD_DOWN   # if a high or a low should avtivate it

pi.set_mode(servoCheck1, pigpio.INPUT)
pi.set_mode(servoCheck2, pigpio.INPUT)
pi.set_mode(sensorEcho, pigpio.INPUT)
pi.set_mode(sensorTrigger, pigpio.OUTPUT)

pi.set_pull_up_down(servoCheck1, pud)
pi.set_pull_up_down(servoCheck2, pud)
pi.set_pull_up_down(sensorEcho, pud)


def setServo(angle):
    if (angle > 180):   # Define scope for the angles
        angle = 180
    elif (angle < 0):
        angle = 0

    pulse1 = (angle / 180)*1800 + 550     # Translate angle to duty value
    pulse2 = 2350 - (angle / 180)*1800
    pi.set_servo_pulsewidth(servoPin1, pulse1)    # Change pwm to calculated value
    pi.set_servo_pulsewidth(servoPin2, pulse2)

def getServo():
    s1 = 0
    s2 = 0
    for i in range(50):
        s1 += pi.read(servoCheck1)
        s2 += pi.read(servoCheck2)
    return [s1,s2]

def checkDistance(distance):
    pi.write(TRIG, 1)
    time.sleep(0.00001)
    pi.write(TRIG, 0)

    while pi.read(ECHO)==0:
        pulse_start = time.time()

    while pi.read(ECHO)==1:
        pulse_end = time.time()

    pulseTime = (pulse_end - (pulse_start/2))
    waterheight = (distance - (pulseTime*34300))
    return waterheight
