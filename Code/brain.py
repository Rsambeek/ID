from helper2 import *


cycleIndex = 0
while True:
    if node.attrs['Spec']['Labels']['inspectorgadget'] == 'True' and cycleIndex%2 == 0:
        if cycleIndex = 10
            dbCursor.execute("SELECT setting, value FROM settings WHERE setting = sensorHeight OR setting = trigger")
            sensorHeight = dbCursor.fetchall()[0][1]
            triggerHeight = dbCursor.fetchall()[1][1]
            cycleIndex = 0
        cycleIndex +=1

        waterHeight = checkDistance(sensorHeight)
        dbCursor.execute("SELECT MAX(Timestamp), Value, GateDecision FROM waterheight")	# Get waterheight from database
        inspectorgadgetDesision = dbCursor.fetchall()[1]
        if inspectorgadgetDesision[1] != waterHeight or inspectorgadgetDesision[2] != (1 if waterHeight > triggerHeight else 0):
            dbCursor.execute("INSERT INTO interventions (Intervention) VALUES(inspectorgadget)")
            time.sleep(10)
            dbCursor.execute("SELECT * FROM interventions WHERE  Timestamp >= NOW() - INTERVAL 10 SECOND AND Intervention = inspectorgadget")
            interventions = len(dbCursor.fetchall())	# Get ammount of new interventions
            if interventions < (len(client.nodes.list())/2):    # If more interventions demote yourself from gatekeeper
                dbCursor.execute(str("INSERT INTO error (Hostname, ErrorType) VALUES("+socket.gethostname()+",Gatekeeper lost da wae)))
                node.update({'Availability': 'active', 'Name': 'Name': socket.gethostname(),'Role': 'manager','Labels': {'inspectorgadget':'False'}})
                os.system('sudo reboot now')

    if node.attrs['Spec']['Labels']['gatereader'] == 'True' and cycleIndex%2 == 1:
        servoPos = getServo()
        if servoPos[0] > 0 or servoPos[1] > 0:
            dbCursor.execute("INSERT INTO interventions (Intervention) VALUES(gatekeeper)")
            time.sleep(10)
            dbCursor.execute("SELECT * FROM interventions WHERE  Timestamp >= NOW() - INTERVAL 10 SECOND AND Intervention = gatekeeper")
            interventions = len(dbCursor.fetchall())	# Get ammount of new interventions
            if interventions < (len(client.nodes.list())/2):    # If more interventions demote yourself from gatekeeper
                dbCursor.execute(str("INSERT INTO error (Hostname, ErrorType) VALUES("+socket.gethostname()+",Gatekeeper lost da wae)))
                node.update({'Availability': 'active', 'Name': socket.gethostname(),'Role': 'manager','Labels': {'inspectorgadget':'False'}})
                os.system('sudo reboot now')


    time.sleep(1)
