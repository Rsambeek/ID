from helper import *


cycleIndex = 10
while True:
    if cycleIndex == 10:
        db = MySQLdb.connect(host='den1.mysql1.gear.host', user='waterratjes', passwd='Ke3Yq_h_Z478',db='waterratjes')
        dbCursor = db.cursor()
        dbCursor.execute("SELECT setting, value FROM settings WHERE setting = sensorHeight OR setting = trigger")
        sensorHeight = dbCursor.fetchall()[0][1]
        triggerHeight = dbCursor.fetchall()[1][1]
        cycleIndex = 1

    waterHeight = checkDistance(sensorHeight)
    db = MySQLdb.connect(host='den1.mysql1.gear.host', user='waterratjes', passwd='Ke3Yq_h_Z478',db='waterratjes')
    dbCursor = db.cursor()
    dbCursor.execute("INSERT INTO waterheight (value, GateDecision) VALUES ("+waterHeight+", 1 if "+waterHeight+" > "+triggerHeight+" else 0)")

    time.sleep(2)

    db = MySQLdb.connect(host='den1.mysql1.gear.host', user='waterratjes', passwd='Ke3Yq_h_Z478',db='waterratjes')
    dbCursor = db.cursor()
    dbCursor.execute("SELECT * FROM interventions WHERE  Timestamp >= NOW() - INTERVAL 10 SECOND AND Intervention = inspectorgadget")
    interventions = len(dbCursor.fetchall())	# Get ammount of new interventions
    if interventions > (len(client.nodes.list())/2):    # If more interventions demote yourself from gatekeeper
        db = MySQLdb.connect(host='den1.mysql1.gear.host', user='waterratjes', passwd='Ke3Yq_h_Z478',db='waterratjes')
        dbCursor = db.cursor()
        dbCursor.execute(str("INSERT INTO error (Hostname, ErrorType) VALUES("+socket.gethostname()+"Inspectorgadget lost da wae)"))
        node.update({'Availability': 'active', 'Name': socket.gethostname(),'Role': 'manager','Labels': {'Inspectorgadget':'False'}})
        os.system('sudo reboot now')
