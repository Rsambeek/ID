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

while True:
    if node.attrs['Spec']['Labels']['inspectorgadget'] == 'True':
        cycleIndex = 1
        while True:
            if cycleIndex = 10
                dbCursor.execute("SELECT setting, value FROM settings WHERE setting = sensorHeight OR setting = trigger")
                sensorHeight = dbCursor.fetchall()[0][1]
                triggerHeight = dbCursor.fetchall()[1][1]
                cycleIndex = 1

            waterHeight = checkDistance(sensorHeight)
            dbCursor.execute("SELECT MAX(Timestamp), Value, GateDecision FROM waterheight")	# Get waterheight from database
            inspectorgadgetDesision = dbCursor.fetchall()[1]
            if inspectorgadgetDesision[1] != waterHeight or inspectorgadgetDesision[2] != (1 if waterHeight > triggerHeight else 0):
                dbCursor.execute("INSERT INTO interventions (Intervention) VALUES(inspectorgadget)")

            time.sleep(2)
