from Servo import *
import socket
import docker
import time
import MySQLdb



def gatestate(val):	# Translate boolean to "open" or "close" text
    return "close" if bool(val) else "open"


while True:	# Database connection loopst infinite times to make sure there is a connection
    try:
        db = MySQLdb.connect(host='den1.mysql1.gear.host', user='waterratjes', passwd='Ke3Yq_h_Z478',db='waterratjes')
        dbCursor = db.cursor()
        break
    except MySQLdb.Error:	# If for some reason there cant be a connection just pass the exception to retry
        pass

print("Database connection established\nStarting gate keeping")


client = docker.from_env()	# Get current client in docker swarm

while True:	# Infitly loop to update motor position
#for i in range(5): # Testing purposes only!
    dbCursor.execute("SELECT MAX(Timestamp), GateDecision FROM waterheight")	# Get waterheight from database

    for row in dbCursor.fetchall():	# Get latest height added to database
        gateState = bool(row[1])

        if gateState:	# Set motor to position
            setServo(0)
        else:
            setServo(90)
        print("Gate", gatestate(gateState))

        time.sleep(2)
        break

	# Get interventions from database to check if working correct
    dbCursor.execute("SELECT * FROM interventions WHERE  Timestamp >= NOW() - INTERVAL 10 SECOND")
    interventions = len(dbCursor.fetchall())	# Get ammount of new interventions
    if interventions > (len(client.nodes.list())/2):    # If more interventions demote yourself from gatekeeper
        dbCursor.execute(str("INSERT INTO error (Hostname, ErrorType) VALUES("+socket.gethostname()+",Gatekeeper lost da wae)))
        node = client.nodes.get(socket.gethostname())
        node.update({'Availability': 'active', 'Name': 'node-name','Role': 'manager','Labels': {'gatekeeper':'False'}})
