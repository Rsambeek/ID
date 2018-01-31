from helper import *    # Imports all the modules needed


def gatestate(val):	# Translate boolean to "open" or "close" text
    return "close" if bool(val) else "open"


print("Starting gate keeping")

while True:	# Infitly loop to update motor position
#for i in range(5): # Testing purposes only!
    dbCursor.execute("SELECT Timestamp, GateDecision FROM waterheight ORDER BY Timestamp DESC LIMIT 1")	# Get desired gate state from database

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
    dbCursor.execute("SELECT * FROM interventions WHERE  Timestamp >= NOW() - INTERVAL 10 SECOND AND Intervention = gatekeeper")
    interventions = len(dbCursor.fetchall())	# Get ammount of new interventions
    if interventions > (len(client.nodes.list())/2):    # If more interventions demote yourself from gatekeeper
        dbCursor.execute(str("INSERT INTO error (Hostname, ErrorType) VALUES("+socket.gethostname()+"Gatekeeper lost da wae)"))
        node.update({'Availability': 'active', 'Name': socket.gethostname(),'Role': 'manager','Labels': {'gatekeeper':'False'}})
        os.system('sudo reboot now')
