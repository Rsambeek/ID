from helper import *


cycleIndex = 1
while True:
    if cycleIndex == 10:
        dbCursor.execute("SELECT setting, value FROM settings WHERE setting = sensorHeight OR setting = trigger")
        sensorHeight = dbCursor.fetchall()[0][1]
        triggerHeight = dbCursor.fetchall()[1][1]
        cycleIndex = 1

    waterHeight = checkDistance(sensorHeight)
    dbCursor.execute("INSERT INTO waterheight (value, GateDecision) VALUES ("waterHeight", 1 if "waterHeight" > "triggerHeight" else 0)")

    time.sleep(2)

    dbCursor.execute("SELECT * FROM interventions WHERE  Timestamp >= NOW() - INTERVAL 10 SECOND AND Intervention = inspectorgadget")
    interventions = len(dbCursor.fetchall())	# Get ammount of new interventions
    if interventions > (len(client.nodes.list())/2):    # If more interventions demote yourself from gatekeeper
        dbCursor.execute(str("INSERT INTO error (Hostname, ErrorType) VALUES("+socket.gethostname()+"Inspectorgadget lost da wae)"))
        node.update({'Availability': 'active', 'Name': socket.gethostname(),'Role': 'manager','Labels': {'Inspectorgadget':'False'}})
        os.system('sudo reboot now')
