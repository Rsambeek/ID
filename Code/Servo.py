import time
import wiringpi

servoPin1 = 18  #Setup variables for pins for servo's
servoPin2 = 19

wiringpi.wiringPiSetupGpio()    # Setup wiringpi to use gpio layout and not pin layout
wiringpi.pinMode(servoPin1, wiringpi.GPIO.PWM_OUTPUT)   # Setup servo pins as Pulse Width Modulation pins
wiringpi.pinMode(servoPin2, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)

delay_period = 0.01

def setServo(angle):
    if (angle > 180):   # Define scope for the angles
        angle = 180
    elif (angle < 0):
        angle = 0

    pulse1 = (angle/180*200)+50     # Translate angle to pwm value
    pulse2 = 250-(angle/180*200)
    wiringpi.pwmWrite(servoPin1, pulse1)    # Change pwm to calculated value
    wiringpi.pwmWrite(servoPin2, pulse2)
