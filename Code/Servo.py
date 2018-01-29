import time
from RPi import GPIO

GPIO.setwarnings(False)

servoPin1 = 12  #Setup variables for pins for servo's
servoPin2 = 16

GPIO.setmode(GPIO.BOARD)    # Setup wiringpi to use gpio layout and not pin layout
GPIO.setup(servoPin1, GPIO.OUT) # Setup servo pins as output pins
GPIO.setup(servoPin2, GPIO.OUT)
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
