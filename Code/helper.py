import time
from RPi import GPIO

GPIO.setwarnings(False)

servoPin1 = 29  #Setup variables for pins for servo's
servoPin2 = 31
servoCheck1 = 33
servoCheck2 = 35
sensorTrigger = 32
sensorEcho = 36

GPIO.setmode(GPIO.BOARD)    # Setup gpio to use pin layout
GPIO.setup(servoPin1, GPIO.OUT) # Setup servo pins as output pins
GPIO.setup(servoPin2, GPIO.OUT)
GPIO.setup(servoCheck1, GPIO.IN)
GPIO.setup(servoCheck2, GPIO.IN)
GPIO.setup(sensorTrigger, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(sensorEcho, GPIO.IN)
s1 = GPIO.PWM(servoPin1, 100)   # Setup servo pins as Pulse Width Modulation pins
s2 = GPIO.PWM(servoPin2, 100)   # 100 indicates 100Hz so every cycle is 10 miliseconds
s1.start(1)     #percentage of time per cycle that the pin is high
s2.start(1)

def setServo(angle):
    if (angle > 180):   # Define scope for the angles
        angle = 180
    elif (angle < 0):
        angle = 0

    duty1 = angle / 180 + 1     # Translate angle to duty value
    duty2 = 2 - angle / 180
    s1.ChangeDutyCycle(duty1)    # Change pwm to calculated value
    s2.ChangeDutyCycle(duty2)

def getServo():
    for i in range(50):
        GPIO.input(servoCheck1)
        GPIO.input(servoCheck2)

def checkDistance(distance):
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    pulseTime = (pulse_end - (pulse_start/2))
    waterheight = (distance - (pulseTime*34300))
    return waterheight
