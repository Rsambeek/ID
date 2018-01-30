import time
import wiringpi
import socket
import docker
import os
import MySQLdb


try:
    node.attrs['Spec']['Labels']['inspectorgadget']
except:
    print("Label inspectorgadget not found\nCreating now")
    node.update({'Availability': 'active', 'Name': socket.gethostname(), 'Role': 'manager', 'Labels': {'inspectorgadget': 'True'}})

try:
    node.attrs['Spec']['Labels']['gatekeeper']
except:
    print("Label gatekeeper not found\nCreating now")
    node.update({'Availability': 'active', 'Name': socket.gethostname(), 'Role': 'manager', 'Labels': {'gatekeeper': 'True'}})

try:
    node.attrs['Spec']['Labels']['gatereader']
except:
    print("Label gatekeeper not found\nCreating now")
    node.update({'Availability': 'active', 'Name': socket.gethostname(), 'Role': 'manager', 'Labels': {'gatekeeper': 'gatereader'}})


while True:     # Database connection loopst infinite times to make sure there is a connection
    try:
        db = MySQLdb.connect(host='den1.mysql1.gear.host', user='waterratjes', passwd='Ke3Yq_h_Z478',db='waterratjes$')
        dbCursor = db.cursor()
        print("Database connection established")
        break
    except MySQLdb.Error:       # If for some reason there cant be a connection just pass the exception to retry
        pass

client = docker.from_env()	# Get current client
node = client.nodes.get(socket.gethostname())   # get current node in docker swarm


servoPin1 = 15  #Setup variables for pins for servo's
servoPin2 = 16
servoCheck1 = 29
servoCheck2 = 31
sensorTrigger = 32
sensorEcho = 35

wiringpi.wiringPiSetup()    # Setup gpio to use pin layout
wiringpi.pinMode(servoPin1, 1) # Setup servo pins as output pins
wiringpi.pinMode(servoPin2, 1)
wiringpi.pinMode(servoCheck1, 0)
wiringpi.pinMode(servoCheck2, 0)
wiringpi.pinMode(sensorTrigger, 1)
wiringpi.pinMode(sensorEcho, 0)
wiringpi.softPwmCreate(servoPin1, 0, 100)
wiringpi.softPwmCreate(servoPin2, 0, 100)


def setServo(angle):
    if (angle > 180):   # Define scope for the angles
        angle = 180
    elif (angle < 0):
        angle = 0

    pulse1 = angle / 180 + 1     # Translate angle to duty value
    pulse2 = 2 - angle / 180
    wiringpi.softPwmWrite(servoPin1, pulse1)    # Change pwm to calculated value
    wiringpi.softPwmWrite(servoPin2, pulse2)

def getServo():
    s1 = 0
    s2 = 0
    for i in range(50):
        s1 += bin(wiringpi.digitalRead(servoCheck1))
        s2 += bin(wiringpi.digitalRead(servoCheck2))
    return [s1,s2]

def checkDistance(distance):
    wiringpi.digitalWrite(TRIG, 1)
    time.sleep(0.00001)
    wiringpi.digitalWrite(TRIG, 0)

    while wiringpi.digitalRead(ECHO)==0:
        pulse_start = time.time()

    while wiringpi.digitalRead(ECHO)==1:
        pulse_end = time.time()

    pulseTime = (pulse_end - (pulse_start/2))
    waterheight = (distance - (pulseTime*34300))
    return waterheight
