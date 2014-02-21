#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import json

with open('sensors.json') as jsonFile
	sensorData = json.load(jsonFile)

jsonFile.close()

for item in sensorData["sensors"]:
    print item["Id"]
	print item["SensorName"]
	print item["SensorSerialNo"]
	print item["MinValue"]
	print item["MaxValue"]