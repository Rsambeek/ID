# import Servo.py   #Uncomment all servo related code when using on raspberry pi
import threading

height = 0
stopThread = False

def updateServo():
    global height
    action = False  # Temp variable to replace the servo
    for i in range(200):
        if not stopThread:
            # some action to get water height in some value
            
            if height < 50:
                action = True# Temp variable to replace the servo
                # Servo.setServo(0)
            else:
                action = False# Temp variable to replace the servo
                # Servo.setServo(90)
            print(threading.currentThread().getName(), action)
        else:
            break

t = threading.Thread(name="Thread1",target=updateServo)    #setting up a thread
t.start()

stopThread = True   # How to stop the threads
