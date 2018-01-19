import Servo   #Uncomment all servo related code when using on raspberry pi
import threading

height = 0
stopThread = False

def updateServo():
    global height
    for i in range(200):
        if stopThread:
            break
        else:
            # some action to get water height in some value

            if height < 50:
                Servo.setServo(0)
            else:
                Servo.setServo(90)
            print(threading.currentThread().getName(), height)

            keys = input("Enter")
            if keys == "S":
                break
            else:
                height = keys

t = threading.Thread(name="Thread1",target=updateServo)    #setting up a thread
t.start()

# stopThread = True   # How to stop the threads
