from helper import *


cycleIndex = 10
while True:
    db = MySQLdb.connect(host='den1.mysql1.gear.host', user='waterratjes', passwd='Ke3Yq_h_Z478',db='waterratjes')
    dbCursor = db.cursor()
    if node.attrs['Spec']['Labels']['inspectorgadget'] == 'True' and cycleIndex%2 == 0:
        if cycleIndex == 10:
            dbCursor.execute("SELECT setting, value FROM settings")
            for data in dbCursor.fetchall():
                if data[0] == "sensorHeight":
                    sensorHeight = data[1]
                elif data[0] == "trigger":
                    triggerHeight = data[1]
            cycleIndex = 0
        cycleIndex +=1

        waterHeight = checkDistance(sensorHeight)
        dbCursor.execute("SELECT Timestamp, Value, GateDecision FROM waterheight ORDER BY Timestamp DESC LIMIT 1")	# Get waterheight from database
        inspectorgadgetDesision = dbCursor.fetchall()[1]
        if inspectorgadgetDesision[1] != waterHeight or inspectorgadgetDesision[2] != (1 if waterHeight > triggerHeight else 0):
            dbCursor.execute("INSERT INTO interventions (Intervention) VALUES('inspectorgadget')")
            db.commit()
            time.sleep(10)
            db = MySQLdb.connect(host='den1.mysql1.gear.host', user='waterratjes', passwd='Ke3Yq_h_Z478',db='waterratjes')
            dbCursor = db.cursor()
            dbCursor.execute("SELECT * FROM interventions WHERE  Timestamp >= NOW() - INTERVAL 10 SECOND AND Intervention = 'inspectorgadget'")
            interventions = len(dbCursor.fetchall())	# Get ammount of new interventions
            if interventions < (len(client.nodes.list())/2):    # If more interventions demote yourself from gatekeeper
                labels['inspectorgadget'] = 'False'
                dbCursor.execute("INSERT INTO errors (Hostname, ErrorType) VALUES('{0}', ' Stopped inspecting sensor')".format(socket.gethostname()))
                db.commit()
                labels['inspectorgadget'] = 'False'
                node.update({'Availability': 'active', 'Name': socket.gethostname(),'Role': 'manager','Labels': labels})
                os.system('sudo reboot now')

    if node.attrs['Spec']['Labels']['gatereader'] == 'True' and cycleIndex%2 == 1:
        servoPos = getServo()
        print(servoPos)
        if servoPos[0] == 0 or servoPos[1] == 0:
            dbCursor.execute("INSERT INTO interventions (Intervention) VALUES('gatekeeper')")
            db.commit()
            time.sleep(10)
            dbCursor.execute("SELECT * FROM interventions WHERE  Timestamp >= NOW() - INTERVAL 10 SECOND AND Intervention = 'gatekeeper'")
            interventions = len(dbCursor.fetchall())	# Get ammount of new interventions
            print(interventions, len(client.nodes.list())/2)
            if interventions < (len(client.nodes.list())/2):    # If more interventions demote yourself from gatekeeper
                labels['gatereader'] = 'False'
                dbCursor.execute("INSERT INTO errors (Hostname, ErrorType) VALUES('{0}', ' Stopped reading gates')".format(socket.gethostname()))
                db.commit()
                labels['gatereader'] = 'False'
                node.update({'Availability': 'active', 'Name': socket.gethostname(),'Role': 'manager','Labels': labels})
                os.system('sudo reboot now')

    time.sleep(1)
    cycleIndex +=1
