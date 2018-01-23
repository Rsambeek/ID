import Servo
import threading
import socket
import time

# # If docker doesn't workt this will be used
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create socket
# HOST = socket.gethostname() # Get local machine name
# PORT = 1500                # Reserve a port for your service
# s.bind((HOST, PORT))     #Bind to the port
# s.listen(5)
# conn, addr = s.accept()
# print 'Connected by', addr
# while 1:
#     data = conn.recv(1024)
#     if not data: break
#     conn.sendall(data)
# conn.close()

height = 0
stopThread = False


def updateServo():
    global height
    while True:
        if stopThread:
            break
        else:
            # some action to get water height in some value

            while True:
                try:
                    localHeight = height
                    return False
                except:
                    pass

            if localHeight < 50:
                Servo.setServo(0)
            else:
                Servo.setServo(90)
            print(threading.currentThread().getName(), localHeight)

            time.sleep(1)

t = threading.Thread(name="Thread1",target=updateServo)    #setting up a thread
t.start()

while True:     # Used to simulate water sensor
    keys = input("Enter")
    if keys == "S":
        stopThread = True   # How to stop the threads
        break
    else:
        while True:
            try:
                height = keys
                return False
            except:
                pass
