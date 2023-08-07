import psycopg2
import requests
from flask import Flask, render_template, session, redirect, url_for, flash
import os
from flask_assets import Environment, Bundle
import json
from flask import *
import time


#global variables: 
masterbedEvents = {"window1": 1, "tv": 4, "window2": 2, "lamp1": 5, "door1": 14, "roomLight": 19}
bed2Events = {"window1": 1, "window2": 2, "lamp1": 5, "lamp2": 6, "door1": 14, "roomLight": 19}
bed3Events = {"window1": 1,"window2": 2, "lamp1": 5,"lamp2": 6 ,"door1": 14, "roomLight": 19}
bathroom1Events = {"overheadLight": 7,"exhaustFan": 8, "window1": 1, "door1": 14, "washingMachine": 17, "dryer": 18, "roomLight": 19, "faucet": 20, "shower": 21}
bathroom2Events = {"overheadLight": 7,"exhaustFan": 8, "window1": 1, "door1": 14, "roomLight": 19, "faucet": 20}
kitchenEvents = {"overheadLight": 7, "stove": 9, "oven": 10, "microwave": 11, "refrigerator": 12, "dishwasher": 13, "window1": 1, "window2": 2, "roomLight": 19}
livingroomEvents = {"overheadLight": 7, "lamp1": 5, "lamp2": 6, "tv": 4, "window1": 1, "window2": 2, "window3": 3, "roomLight": 19}
garageEvents = {"door1": 14, "door2": 15, "roomLight": 19}
pointsOfEntryEvents = {"door1": 14, "door2": 15, "door3": 16, "roomLight": 19}


roomEventPrimeKeys = {
    "window1": 1,
    "window2": 2,
    "window3": 3,
    "tv": 4,
    "lamp1": 5,
    "lamp2": 6,
    "overheadLight": 7,
    "exhaustFan": 8,
    "stove": 9,
    "oven": 10,
    "microwave": 11,
    "refrigerator": 12,
    "dishwasher": 13,
    "door1": 14,
    "door2": 15, 
    "door3": 16,
    "washingMachine": 17,
    "dryer": 18,
    "roomLight": 19,
    "faucet": 20,
    "shower": 21,
    "thermostat": 22
}

roomType = ["masterbed", "bed2", "bed3", "bathroom1", "bathroom2", "livingroom", "kitchen", "garage", "pointofentry"]

allValues = {}
request_data = ""
value = 15
outdoorEvent = 0


DB_NAME = "Team4DB"
DB_USER = "Team4"
DB_PASS = "Team4"
DB_PORT = "5432"
DB_HOST = "138.26.48.83"
roomNameLightEvent = []
lightRoom = ""
RUNONCE = True
 
# will return connection object when calling connect
conn = psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASS, port=DB_PORT, host=DB_HOST)

# print("PostgreSQL server information")
# print(conn.get_dsn_parameters(), "\n")

curr = conn.cursor()

# eventTable = '''CREATE TABLE Events (
# 	id serial PRIMARY KEY ,
# 	eventType VARCHAR (100) NOT NULL
# )'''

# curr.execute(eventTable)
# conn.commit()




# logsTable = '''CREATE TABLE Logs (
# 	id serial PRIMARY KEY,
# 	eventType INT,
# 	eventDate DATE,
# 	eventTime TIME,
# 	eventDuration INT,
# 	eventState VARCHAR (100),
# 	roomType VARCHAR (100))'''


# curr.execute(logsTable)
# conn.commit()







def makeAllLogsFinished():
	sql = "UPDATE Logs SET eventState = %s WHERE eventState = %s"
	curr.execute(sql, ("FINISHED","RUNNING"))
	conn.commit()



if (RUNONCE == True):
	RUNONCE = False
	makeAllLogsFinished()



def convertFetchTupleToDict(tup):
	dictionary = {}
	keys = ['eventDate','eventTime','eventDuration','eventState','roomType','eventType']
	index = 0
	for i in tup:
		val = keys[index]
		dictionary[val] = i
		index+=1
	return dictionary
		

def returnValueNone():
	dictionary = {}
	keys = ['eventDate','eventTime','eventDuration','eventState','roomType','eventType']
	index = 0
	for i in range(len(keys)):
		val = keys[i]
		dictionary[val] = "None"
	return dictionary



# need to make Logs.eventDate & Logs.eventTime into strings
def fetchLastLoggedEvent(event, room):
	vals = {}	
	sql = "SELECT CAST(Logs.eventDate AS VARCHAR), CAST(Logs.eventTime AS VARCHAR), Logs.eventDuration,Logs.eventState, Logs.roomType, Events.eventType FROM Logs INNER JOIN Events ON Logs.eventType = Events.id AND Logs.roomType = %s AND Logs.eventType = %s ORDER BY eventDate DESC, eventTime DESC FETCH FIRST %s ROWS ONLY"
	curr.execute(sql, (room,event,1))
	tup = curr.fetchone()
	# conn.commit()
	if tup == None:
		return returnValueNone()
	value = convertFetchTupleToDict(tup)
	return value






def gatherAllDataForRoom(roomEventlist, roomType):
	lst = []
	dct = {}
	#loop through keys and values
	for key,value in roomEventlist.items():
		logEvent = fetchLastLoggedEvent(value,roomType)
		dct[key] = logEvent
	return dct







def writeToDataBase(log):
	curr.execute("INSERT INTO Logs (eventType, eventDate,eventTime,eventDuration, eventState, roomType) VALUES (%s, %s, %s, %s, %s,%s)", 
				(log["eventType"], log["eventDate"],log["eventTime"],log["eventDuration"],log["eventState"],log["roomType"]))
	conn.commit()



def writeToEventTypeDatabase(eventType):
	curr.execute("INSERT INTO Events (eventType) VALUES (%s)", (eventType,))
	conn.commit()








def updateStateInDatabase(log):
	sql = "UPDATE Logs SET eventState = %s WHERE eventState = %s"
	curr.execute(sql, ("FINISHED","RUNNING"))
	conn.commit()



def LogsDatabaseRecords():
	curr.execute('SELECT * FROM Logs')
	lst = curr.fetchall()
	for i in range(len(lst)):
		print(lst[i])
		print("******************\n")

def EventsDatabaseRecords():
	curr.execute('SELECT * FROM Events')
	lst = curr.fetchall()
	for i in range(len(lst)):
		print(lst[i])
		print("******************\n")




basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)


# LogsDatabaseRecords()
# EventsDatabaseRecords()
# logEvent = fetchLastLoggedEvent(19, "garage")
# updateStateInDatabase(logEvent)
# LogsDatabaseRecords()



@app.route('/',methods=['GET'])
def screen1():
	return render_template('index.html')




@app.route('/screen2',methods=['GET'])
def screen2():
	return render_template('screen2.html')






#how to insert date and time as appropriate data types
@app.route('/lightEvent', methods=['POST'])
def lightEvent():
	if request.method == 'POST':
		request_data = request.get_json()
		log = request_data
		lastLoggedEvent = fetchLastLoggedEvent(log["eventType"], log["roomType"])
		
		if (lastLoggedEvent["eventState"] == "FINISHED" or lastLoggedEvent["eventState"] == "None"):
			writeToDataBase(log)
			time.sleep(5)
			previousLog = fetchLastLoggedEvent(log["eventType"], log["roomType"])
			updateStateInDatabase(previousLog)
			print("done")
	return render_template('lightEvent.html')




@app.route('/temp', methods=['GET', 'POST'])
def tempEvent():
	global outdoorEvent
	if request.method == 'POST':
		request_temp = request.get_json()
		outdoorEvent+= request_temp['number']
		print(outdoorEvent)
	elif request.method == 'GET':
		finalValue = outdoorEvent
		outdoorEvent = 0
		sendValue = {'temp': finalValue}
		return jsonify(sendValue)
	return render_template('temp.html')





@app.route('/screen3', methods=['GET','POST'])
def Screen3Events():
	if request.method == 'POST':
		request_data = request.get_json()
		log = request_data
		lastLoggedEvent = fetchLastLoggedEvent(log["eventType"], log["roomType"])

		if (lastLoggedEvent["eventState"] == "FINISHED" or lastLoggedEvent["eventState"] == "None"):
			writeToDataBase(log)
			time.sleep(8)
			previousLog = fetchLastLoggedEvent(log["eventType"], log["roomType"])
			updateStateInDatabase(previousLog)
			print("done")
	return render_template('screen3.html')
	



# add garage and pointsofentry
@app.route('/checkRoom', methods=['GET','POST'])
def checkRoom():
	global allValues
	if request.method == 'POST':
		request_data = request.get_json()
		room = request_data["roomType"]
		if (room == "masterbed"):
			allValues = gatherAllDataForRoom(masterbedEvents, room)
		elif (room == "bed2"):
			allValues = gatherAllDataForRoom(bed2Events, room)
		elif (room == "bed3"):
			allValues = gatherAllDataForRoom(bed3Events, room)
		elif room == "kitchen":
			allValues = gatherAllDataForRoom(kitchenEvents, room)
		elif room == "livingroom":
			allValues = gatherAllDataForRoom(livingroomEvents, room)
		elif room == "garage":
			allValues = gatherAllDataForRoom(garageEvents, room)
		elif room == "bathroom1":
			allValues = gatherAllDataForRoom(bathroom1Events, room)
		elif room == "bathroom2":
			allValues = gatherAllDataForRoom(bathroom2Events, room)
		elif room == "pointofentry":
			allValues = gatherAllDataForRoom(pointsOfEntryEvents, room)


		
	else:
		return jsonify(allValues)

	return render_template('checkRoom.html')







# def getWaterDataByMonth(monthNum):
# 	returnVal = []
# 	sql = ""
# 	tup = None
# 	tup2 = None
# 	tup3 = None
# 	if (monthNum == 12):
# 		sql1 = "SELECT CAST(eventDate AS VARCHAR), CAST(eventTime AS VARCHAR), eventDuration,eventState, roomType, eventType FROM Logs WHERE eventDate >= to_date('2022-12-01','YYYY-MM-DD') AND eventType = %s ORDER BY eventDate ASC"
# 		sql2 = "SELECT CAST(eventDate AS VARCHAR), CAST(eventTime AS VARCHAR), eventDuration,eventState, roomType, eventType FROM Logs WHERE eventDate >= to_date('2022-12-01','YYYY-MM-DD') AND eventType = %s ORDER BY eventDate ASC"
# 		sql3 = "SELECT CAST(eventDate AS VARCHAR), CAST(eventTime AS VARCHAR), eventDuration,eventState, roomType, eventType FROM Logs WHERE eventDate >= to_date('2022-12-01','YYYY-MM-DD') AND eventType = %s ORDER BY eventDate ASC"
# 		curr.execute(sql1,(17,))
# 		tup = curr.fetchall()
# 		curr.execute(sql2,(20,))
# 		tup2 = curr.fetchall()
# 		curr.execute(sql3,(21,))
# 		tup3 = curr.fetchall()

# 	else:
# 		sql1 = "SELECT CAST(eventDate AS VARCHAR), CAST(eventTime AS VARCHAR), eventDuration,eventState, roomType, eventType FROM Logs WHERE eventDate > to_date('2022-%s-01','YYYY-MM-DD') AND eventDate < to_date('2022-%s-01','YYYY-MM-DD') AND eventType = %s ORDER BY eventDate ASC"
# 		sql2 = "SELECT CAST(eventDate AS VARCHAR), CAST(eventTime AS VARCHAR), eventDuration,eventState, roomType, eventType FROM Logs WHERE eventDate > to_date('2022-%s-01','YYYY-MM-DD') AND eventDate < to_date('2022-%s-01','YYYY-MM-DD') AND eventType = %s ORDER BY eventDate ASC"
# 		sql3 = "SELECT CAST(eventDate AS VARCHAR), CAST(eventTime AS VARCHAR), eventDuration,eventState, roomType, eventType FROM Logs WHERE eventDate > to_date('2022-%s-01','YYYY-MM-DD') AND eventDate < to_date('2022-%s-01','YYYY-MM-DD') AND eventType = %s ORDER BY eventDate ASC"
	
# 		curr.execute(sql1,(monthNum,monthNum+1, 17))
# 		tup = curr.fetchall()
# 		curr.execute(sql2,(monthNum,monthNum+1, 20))
# 		tup2 = curr.fetchall()
# 		curr.execute(sql3,(monthNum,monthNum+1, 21))
# 		tup3 = curr.fetchall()
	
# 	for i in range(len(tup)):
# 		val = convertFetchTupleToDict(tup[i])
# 		returnVal.append(val)

# 	for i in range(len(tup2)):
# 		val = convertFetchTupleToDict(tup2[i])
# 		returnVal.append(val)

# 	for i in range(len(tup3)):
# 		val = convertFetchTupleToDict(tup3[i])
# 		returnVal.append(val)
		
# 	return returnVal




def getWaterDataByMonth(monthNum):
	returnVal = []
	sql = ""
	if (monthNum == 12):
		sql = '''SELECT CAST(eventDate AS VARCHAR), CAST(eventTime AS VARCHAR), eventDuration,eventState, roomType, eventType FROM Logs WHERE eventDate >= to_date('2022-12-01','YYYY-MM-DD') 
				AND eventType != %s 
				AND eventType != %s 
				AND eventType != %s 
				AND eventType != %s 
				AND eventType != %s 
				AND eventType != %s 
				AND eventType != %s 
				AND eventType != %s 
				AND eventType != %s 
				AND eventType != %s 
				AND eventType != %s 
				AND eventType != %s 
				AND eventType != %s 
				AND eventType != %s 
				AND eventType != %s 
				AND eventType != %s 
				AND eventType != %s 
				AND eventType != %s 
				AND eventType != %s 
				ORDER BY eventDate ASC'''
		curr.execute(sql,(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,19,22,))
	else:
		sql = '''SELECT CAST(eventDate AS VARCHAR), CAST(eventTime AS VARCHAR), eventDuration,eventState, roomType, eventType FROM Logs WHERE eventDate >= to_date('2022-%s-01','YYYY-MM-DD') AND eventDate < to_date('2022-%s-01','YYYY-MM-DD')
				 AND eventType != %s 
				 AND eventType != %s 
				 AND eventType != %s 
				 AND eventType != %s 
				 AND eventType != %s 
				 AND eventType != %s 
				 AND eventType != %s 
				 AND eventType != %s 
				 AND eventType != %s 
				 AND eventType != %s 
				 AND eventType != %s 
				 AND eventType != %s 
				 AND eventType != %s 
				 AND eventType != %s 
				 AND eventType != %s 
				 AND eventType != %s 
				 AND eventType != %s 
				 AND eventType != %s 
				 AND eventType != %s 
				 ORDER BY eventDate ASC'''
		curr.execute(sql,(monthNum,monthNum+1, 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,19,22,))
	tup = curr.fetchall()
	for i in range(len(tup)):
		val = convertFetchTupleToDict(tup[i])
		returnVal.append(val)
		
	return returnVal



def getElectrictyDataByMonth(monthNum):
	returnVal = []
	sql = ""
	if (monthNum == 12):
		sql = "SELECT CAST(eventDate AS VARCHAR), CAST(eventTime AS VARCHAR), eventDuration,eventState, roomType, eventType FROM Logs WHERE eventDate >= to_date('2022-12-01','YYYY-MM-DD') AND eventType != %s AND eventType != %s AND eventType != %s ORDER BY eventDate ASC"
		curr.execute(sql,(17,20,21,))
	else:
		sql = "SELECT CAST(eventDate AS VARCHAR), CAST(eventTime AS VARCHAR), eventDuration,eventState, roomType, eventType FROM Logs WHERE eventDate >= to_date('2022-%s-01','YYYY-MM-DD') AND eventDate < to_date('2022-%s-01','YYYY-MM-DD') AND eventType != %s AND eventType != %s AND eventType != %s ORDER BY eventDate ASC"
		curr.execute(sql,(monthNum,monthNum+1, 17,20,21))
	tup = curr.fetchall()
	for i in range(len(tup)):
		val = convertFetchTupleToDict(tup[i])
		returnVal.append(val)
		
	return returnVal
	



def getDataForEveryMonth():
	month = 1
	allMonths__water = []
	allMonths__electrcity = []
	val = {}
	for i in range(12):
		water_lst = getWaterDataByMonth(month)
		electricty_lst = getElectrictyDataByMonth(month)
		month+=1
		allMonths__water.append(water_lst)
		allMonths__electrcity.append(electricty_lst)
	val['keys'] = roomEventPrimeKeys
	val['water'] = allMonths__water
	val['electrcity'] = allMonths__electrcity
	return val




@app.route('/data', methods=['GET'])
def DataEvents():
	return jsonify(getDataForEveryMonth())





# test january
# val = getElectrictyDataByMonth(4)

# val = getWaterDataByMonth(4)
# print(LogsDatabaseRecords())
# for i in range(len(val)):
# 	print(val[i])
# 	print('\n')

# print(getDataForEveryMonth())



# sql = "DELETE from Logs WHERE eventDate > to_date('2022-03-05','YYYY-MM-DD') "
# curr.execute(sql,)
# conn.commit()


# sql = "SELECT CAST(eventDate AS VARCHAR), CAST(eventTime AS VARCHAR), eventDuration,eventState, roomType, eventType FROM Logs WHERE eventType = %s"
# curr.execute(sql, (4,))
# tup = curr.fetchall()
# for i in range(len(tup)):
# 	print(tup[i]) 







if __name__ == '__main__':
    app.run(debug=True)





curr.close()
conn.close()
