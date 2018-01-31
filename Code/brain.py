from helper import *


cycleIndex = 10
while True:
    if node.attrs['Spec']['Labels']['inspectorgadget'] == 'True' and cycleIndex%2 == 0:
        if cycleIndex == 10:
            db = MySQLdb.connect(host='den1.mysql1.gear.host', user='waterratjes', passwd='Ke3Yq_h_Z478',db='waterratjes')
            dbCursor = db.cursor()
            dbCursor.execute("SELECT setting, value FROM settings WHERE setting = sensorHeight OR setting = trigger")
            sensorHeight = dbCursor.fetchall()[0][1]
            triggerHeight = dbCursor.fetchall()[1][1]
            cycleIndex = 0
        cycleIndex +=1

        waterHeight = checkDistance(sensorHeight)
        db = MySQLdb.connect(host='den1.mysql1.gear.host', user='waterratjes', passwd='Ke3Yq_h_Z478',db='waterratjes')
        dbCursor = db.cursor()
        dbCursor.execute("SELECT Timestamp, Value, GateDecision FROM waterheight ORDER BY Timestamp DESC LIMIT 1")	# Get waterheight from database
        inspectorgadgetDesision = dbCursor.fetchall()[1]
        if inspectorgadgetDesision[1] != waterHeight or inspectorgadgetDesision[2] != (1 if waterHeight > triggerHeight else 0):
            db = MySQLdb.connect(host='den1.mysql1.gear.host', user='waterratjes', passwd='Ke3Yq_h_Z478',db='waterratjes')
            dbCursor = db.cursor()
            dbCursor.execute("INSERT INTO interventions (Intervention) VALUES(inspectorgadget)")
            time.sleep(10)
            db = MySQLdb.connect(host='den1.mysql1.gear.host', user='waterratjes', passwd='Ke3Yq_h_Z478',db='waterratjes')
            dbCursor = db.cursor()
            dbCursor.execute("SELECT * FROM interventions WHERE  Timestamp >= NOW() - INTERVAL 10 SECOND AND Intervention = inspectorgadget")
            interventions = len(dbCursor.fetchall())	# Get ammount of new interventions
            if interventions < (len(client.nodes.list())/2):    # If more interventions demote yourself from gatekeeper
                db = MySQLdb.connect(host='den1.mysql1.gear.host', user='waterratjes', passwd='Ke3Yq_h_Z478',db='waterratjes')
                dbCursor = db.cursor()
                dbCursor.execute(str("INSERT INTO error (Hostname, ErrorType) VALUES("+socket.gethostname()+"Stopped inspecting sensor)"))
                node.update({'Availability': 'active', 'Name': socket.gethostname(),'Role': 'manager','Labels': {'inspectorgadget':'False'}})
                os.system('sudo reboot now')

    if node.attrs['Spec']['Labels']['gatereader'] == 'True' and cycleIndex%2 == 1:
        servoPos = getServo()
        if servoPos[0] > 0 or servoPos[1] > 0:
            db = MySQLdb.connect(host='den1.mysql1.gear.host', user='waterratjes', passwd='Ke3Yq_h_Z478',db='waterratjes')
            dbCursor = db.cursor()
            dbCursor.execute("INSERT INTO interventions (Intervention) VALUES(gatekeeper)")
            time.sleep(10)
            db = MySQLdb.connect(host='den1.mysql1.gear.host', user='waterratjes', passwd='Ke3Yq_h_Z478',db='waterratjes')
            dbCursor = db.cursor()
            dbCursor.execute("SELECT * FROM interventions WHERE  Timestamp >= NOW() - INTERVAL 10 SECOND AND Intervention = gatekeeper")
            interventions = len(dbCursor.fetchall())	# Get ammount of new interventions
            if interventions < (len(client.nodes.list())/2):    # If more interventions demote yourself from gatekeeper
                db = MySQLdb.connect(host='den1.mysql1.gear.host', user='waterratjes', passwd='Ke3Yq_h_Z478',db='waterratjes')
                dbCursor = db.cursor()
                dbCursor.execute(str("INSERT INTO error (Hostname, ErrorType) VALUES("+socket.gethostname()+"Stoped reading gates)"))
                node.update({'Availability': 'active', 'Name': socket.gethostname(),'Role': 'manager','Labels': {'gatereader':'False'}})
                os.system('sudo reboot now')


    time.sleep(1)
