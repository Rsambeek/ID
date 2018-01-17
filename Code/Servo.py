import time
import wiringpi

servoPin1 = 18
servoPin2 = 19

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(servoPin1, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pinMode(servoPin2, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)

delay_period = 0.01

def setServo(angle):
    if (angle > 180):
        angle = 180
    elif (angle < 0):
        angle = 0

    pulse1 = (angle/180*200)+50
    pulse2 = 250-(angle/180*200)
    wiringpi.pwmWrite(servoPin1, pulse1)
    wiringpi.pwmWrite(servoPin2, pulse2)
