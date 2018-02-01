from helper import *    # Imports all the modules needed


def gatestate(val):	# Translate boolean to "open" or "close" text
    return "close" if bool(val) else "open"


print("Starting gate keeping")

while True:	# Infitly loop to update motor position
#for i in range(5): # Testing purposes only!
    db = MySQLdb.connect(host='den1.mysql1.gear.host', user='waterratjes', passwd='Ke3Yq_h_Z478',db='waterratjes')
    dbCursor = db.cursor()
    dbCursor.execute("SELECT Timestamp, GateDecision FROM waterheight ORDER BY Timestamp DESC LIMIT 1")	# Get desired gate state from database

    for row in dbCursor.fetchall():	# Get latest height added to database
        gateState = bool(row[1])

        if gateState:	# Set motor to position
            setServo(0)
        else:
            setServo(90)
        print("Gate", gatestate(gateState))

        break

    time.sleep(1)
	# Get interventions from database to check if working correct
    dbCursor.execute("SELECT * FROM interventions WHERE  Timestamp >= NOW() - INTERVAL 10 SECOND AND Intervention = 'gatekeeper'")
    interventions = len(dbCursor.fetchall())	# Get ammount of new interventions
    if interventions < (len(client.nodes.list())/2):    # If more interventions demote yourself from gatekeeper
        dbCursor.execute("INSERT INTO errors (Hostname, ErrorType) VALUES('{0},Gatekeeper lost da wae')".format(socket.gethostname()))
        db.commit()
        node.update({'Availability': 'active', 'Name': socket.gethostname(),'Role': 'manager','Labels': labels})
        os.system('sudo reboot now')
