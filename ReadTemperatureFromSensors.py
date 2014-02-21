#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import MySQLdb

db = MySQLdb.connect("localhost", "rpiuser", "devpassword", "RPiDev")
curs=db.cursor()

def parseTemperature( input ):
    secondline = input.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    return temperature / 1000   

def getSensorConfigFile (sensorId):
    sensorPath = "/sys/bus/w1/devices/"+ sensorId +"/w1_slave"
    tfile = open(sensorPath)
    text = tfile.read()
    tfile.close()
    return text

def saveLog(type, description):
    query = """INSERT INTO Logs (lType,lDescription,lDateTime) VALUES(%s,%s,NOW())"""
    curs.execute (query,(type, description))

def checkTemperature(sensorName, temp, sensorMinValue, sensorMaxValue):
    if temp < sensorMinValue:
        print "To cold";

    if temp > sensorMaxValue:
        print "To hot";
    
def saveTemperature(sensorId, sensorName, temp):
    query = """INSERT INTO Temperatures (tSensorId,tDatetime,tTemp) VALUES(%s,NOW(),%s)"""
    curs.execute (query,(sensorId, temp))

def readSensors():
    curs.execute ("""SELECT Id,sSensorSerialNo,sSensorName,sSensorType,sMinValue,sMaxValue from Sensors""")

    for reading in curs.fetchall():
        sensorId = reading["Id"]
        sensorSerialNumber = reading["sSensorSerialNo"]
        sensorName = reading["sSensorName"]
        sensorType = reading["sSensorType"]
        sensorMinValue = reading["sMinValue"]
        sensorMaxValue = reading["sMaxValue"]
        text = getSensorConfigFile(sensorSerialNumber)  
        temp = parseTemperature(text)

        with db:
            if sensorType == "temp":
                print "Sensor: ", sensorName
                print "Temperature: ", temp, "°C\n"
                saveTemperature(sensorId, sensorName, temp)
                checkTemperature(sensorName, temp, sensorMinValue, sensorMaxValue)
                
readSensors()

db.close()
