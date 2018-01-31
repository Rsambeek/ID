from flask import Flask, render_template
import MySQLdb

app = Flask(__name__)


def gatestate(val):	# Translate boolean to "open" or "close" text
    return "close" if bool(val) else "open"


@app.route('/') #sets up internet page
def index():
    while True:  # Database connection loopst infinite times to make sure there is a connection
        try:
            db = MySQLdb.connect(host='den1.mysql1.gear.host', user='waterratjes', passwd='Ke3Yq_h_Z478',
                                 db='waterratjes')
            dbCursor = db.cursor()
            break
        except MySQLdb.Error:
            pass

    dbCursor.execute("SELECT Timestamp, GateDecision, Value FROM waterheight ORDER BY Timestamp DESC LIMIT 1")
    data = dbCursor.fetchall()[0] #code fetches information about the waterkering and links it too waterkering
    if data[1]==0:
        waterkering = 'open'
    else:
        waterkering = 'dicht'
    waterstand = data[2]
    dbCursor.execute("SELECT * FROM errors WHERE Fixed='False'")
    data = dbCursor.fetchall() #code fetches information about errors that may occure in the raspberries
    error = ['No errors']
    if len(data)>0:
        error.pop()
        for device in data:
           error.append('Error {2}: Device {0} has error {1}   '.format(device[1],device[2],data.index(device)+1)) #chooses the part of the tuple needed



    return render_template("index.html" , waterstand=waterstand , waterkering=waterkering , error=str(error).replace("'", '').replace("[", '').replace("]",'')) #renders the code into the htmltemplate and removes unnecessary characters from the error tuple


if __name__ == "__main__": #If the script is imported from another script, the script keeps it given name
    app.run(debug=True)     #debug=True enables errors to appear on the webapp so it helps with the programming
