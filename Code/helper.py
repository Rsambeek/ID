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


while True:     # Database connection loopst infinite times to make sure there is a connection
    try:
        db = MySQLdb.connect(host='den1.mysql1.gear.host', user='waterratjes', passwd='Ke3Yq_h_Z478',db='waterratjes')
        dbCursor = db.cursor()
        print("Database connection established")
        break
    except MySQLdb.Error:       # If for some reason there cant be a connection just pass the exception to retry
        print("Retrying to establish connection")
        pass


servoPin1 = 17  #Setup variables for pins for servo's
servoPin2 = 18
servoCheck1 = 29
servoCheck2 = 31
sensorTrigger = 32
sensorEcho = 35

wiringpi.wiringPiSetupGpio()    # Setup gpio to use pin layout
wiringpi.pinMode(servoPin1, wiringpi.GPIO.PWM_OUTPUT) # Setup servo pins as output pins
wiringpi.pinMode(servoPin2, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pinMode(servoCheck1, 0)
wiringpi.pinMode(servoCheck2, 0)
wiringpi.pinMode(sensorTrigger, 1)
wiringpi.pinMode(sensorEcho, 0)

wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)


def setServo(angle):
    if (angle > 180):   # Define scope for the angles
        angle = 180
    elif (angle < 0):
        angle = 0

    pulse1 = (angle / 180)*200 + 50     # Translate angle to duty value
    pulse2 = 250 - (angle / 180)*200
    wiringpi.pwmWrite(servoPin1, pulse1)    # Change pwm to calculated value
    wiringpi.pwmWrite(servoPin2, pulse2)

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
