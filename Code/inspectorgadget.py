from helper import *


cycleIndex = 10
while True:
    db = MySQLdb.connect(host='den1.mysql1.gear.host', user='waterratjes', passwd='Ke3Yq_h_Z478',db='waterratjes')
    dbCursor = db.cursor()
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
    dbCursor.execute("INSERT INTO waterheight (value, GateDecision) VALUES ("+waterHeight+", 1 if "+waterHeight+" > "+triggerHeight+" else 0)")
    db.commit()

    time.sleep(2)

    dbCursor.execute("SELECT * FROM interventions WHERE  Timestamp >= NOW() - INTERVAL 10 SECOND AND Intervention = inspectorgadget")
    interventions = len(dbCursor.fetchall())	# Get ammount of new interventions
    if interventions > (len(client.nodes.list())/2):    # If more interventions demote yourself from gatekeeper
        dbCursor.execute("INSERT INTO errors (Hostname, ErrorType) VALUES('{0}','Inspectorgadget lost da wae')".format(socket.gethostname()))
        db.commit()
        node.update({'Availability': 'active', 'Name': socket.gethostname(),'Role': 'manager','Labels': labels})
        os.system('sudo reboot now')
