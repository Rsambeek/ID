from helper import *
import socket
import docker
import os
import time
import MySQLdb

while True:     # Database connection loopst infinite times to make sure there is a connection
    try:
        db = MySQLdb.connect(host='den1.mysql1.gear.host', user='waterratjes', passwd='Ke3Yq_h_Z478',db='waterratjes$')
        dbCursor = db.cursor()
        break
    except MySQLdb.Error:       # If for some reason there cant be a connection just pass the exception to retry
        pass

cycleIndex = 1
while True:
    if cycleIndex = 10
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
        dbCursor.execute(str("INSERT INTO error (Hostname, ErrorType) VALUES("+socket.gethostname()+",Gatekeeper lost da wae)))
        node = client.nodes.get(socket.gethostname())
        node.update({'Availability': 'active', 'Name': 'node-name','Role': 'manager','Labels': {'gatekeeper':'False'}})
        os.system('sudo reboot now')
