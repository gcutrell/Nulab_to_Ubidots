import os
import sys
import re
import requests
from datetime import datetime, timedelta
import glob
import time
import json
import traceback

'''
global variables
'''
BASE_DIR=os.path.dirname(os.path.realpath(__file__))
#FolderName = ''			#Use if placed in folder above data.  
ENDPOINT = "industrial.api.ubidots.com"
device = "SanduskyBay_NuLab"
token = "BBFF-3SW5GCgLEF4DVUpYRNMylqFyXAFUDA"	#LTI Token
buoyDateFormat = '%m/%d/%Y %H:%M:%S'


def get_lastSample(url, device, variable,token):
	try:
		url = "https://{}/api/v1.6/devices/{}/{}/lv".format(url,device,variable)
		headers = {"X-Auth-Token": token, "Content-Type": "application/json"}
		attempts = 0
		status_code = 400
		while status_code >= 400 and attempts < 5:
			print("[INFO] Retrieving data, attempt number: {}".format(attempts))
			req = requests.get(url=url, headers=headers)
			status_code = req.status_code
			attempts += 1
			time.sleep(1)

		#print("[INFO] Results:")
		print("Last {} retrieved for {} is {}".format(variable,device,float(req.text)))
		return(float(req.text))
	except Exception as e:
		print("[ERROR] Error posting, details: {}".format(e))

def get_valueExistence(url, variable, dateTime):	
	try:
		url = "https://{}/api/v1.6/devices/{}/{}/values?page=1?page_size=1?start={}?end={}?format=json".format(url,device,variable,dateTime,dateTime)
		headers = {"X-Auth-Token": token, "Content-Type": "application/json"}
		attempts = 0
		status_code = 400
		while status_code >= 400 and attempts < 5:
			#print("[INFO] Retrieving data, attempt number: {}".format(attempts))
			req = requests.get(url=url, headers=headers)
			status_code = req.status_code
			attempts += 1
			time.sleep(1)
		
		#print("[INFO] Results:")
		jsonResponse = json.loads(req.text)
		if (dateTime == jsonResponse["results"][0]["timestamp"]):
			print("Station {} value {} is already up-to-date.".format(device,variable))
			return True
		else:
			print("Station {} value {} is not up-to-date. Adding to payload".format(device,variable))
			return False
		
		return(float(req.text))
	except Exception as e:
		print("[ERROR] Error posting, details: {}. No values may be avaiable for variable {}. Try to add value".format(e,variable))
		return False
		
def getKeyPayload(filePath,channel):
	
	payload = {}

	#Build Array of stations to post to ubidots
	lines = open(filePath).readlines()
	
	#Extract header to be used as key and latestDataRow as value for httppost.
	variables = lines[0].strip().split(",")

	#Remove any paranethesis from variable names to remove changes in units from nulabs
	for i in range(len(variables)):
		variables[i] = variables[i].split('(')[0]

	#If macro header is not listed, then file contains no needed data and skip.
	try:
		macroLoc = variables.index("Macro")
	except: 
		return payload	
	OBSabsLoc = variables.index("OBS_abs")
	OBSconcLoc = variables.index("OBS_conc")
	SmpabsLoc = variables.index("Smp_abs")
	SmpconcLoc = variables.index("Smp_conc")
	LightLoc = variables.index("Light")		 
	macro1 = []
	macro2 = []
	#Reverse lines so the newest data will appear first in array	
	for d in reversed(lines):
		#Will fail for lines were array location does not exist		
		try:
			data = d.strip().split(",")
			if data[macroLoc] == "M1" and data[SmpconcLoc]:
				macro1.append(data)
			elif data[macroLoc] == "M2" and data[OBSconcLoc]:
				macro2.append(data)		
		except:
			pass

	#Check for empty data for macro1 or macro2 results. If empty then return empty payload
	if not macro1 or not macro2:
		return payload

	#Create Unix time in milliseconds from first timestamp always located in first array location
	macro1DateTime = datetime.strptime(macro1[0][0],buoyDateFormat)	
	macro1Timestamp = ((macro1DateTime - datetime(1970,1,1)).total_seconds())*1000
	macro2DateTime = datetime.strptime(macro2[0][0],buoyDateFormat)	
	macro2Timestamp = ((macro2DateTime - datetime(1970,1,1)).total_seconds())*1000

	for x in range(len(variables)):
		#Only need Obs light from Macro2
		if variables[x] in ['OBS_abs','OBS_conc','Light']:
			dateTime = macro2Timestamp
			data = macro2
		elif variables[x] in ['Smp_abs','Smp_conc']:
			dateTime = macro1Timestamp
			data = macro1
		else:
			continue

		paramName = channel+"-"+variables[x]
		updateValue = get_valueExistence("industrial.api.ubidots.com", paramName, dateTime)
		if (updateValue is False):
			#NaN's will cause error. Pass sending variable. 
			try:
				value = float(data[0][x])
				payload[paramName] ={'value':value,'timestamp':dateTime}
			except:
				continue
	return payload
	
def post_var(payload, url, device, token):
	try:
		url = "https://{}/api/v1.6/devices/{}".format(url, device)
		headers = {"X-Auth-Token": token, "Content-Type": "application/json"}
		attempts = 0
		status_code = 400
		print(payload)
		while status_code >= 400 and attempts < 5:
			print("[INFO] Sending data, attempt number: {}".format(attempts))
			req = requests.post(url=url, headers=headers,data=json.dumps(payload))
			status_code = req.status_code
			attempts += 1
			time.sleep(1)

		#print("[INFO] Results:")
		print(req.text)
		print("Data has been succesfully sent to Ubidots for station {}.".format((device)))
	except Exception as e:
		print("[ERROR] Error posting for station {}, details: {}".format(device,e))

	
def main():
    
	print("Runtime at {}.".format(datetime.now()))
	#Get sensor values from each defined buoy file and send to ubidots

	#Retrieve all files that end in .txt. Extract channel type from basename.	
	#dataList = glob.glob(os.path.join(BASE_DIR,FolderName+'/'+'*-L.txt'))	
	dataList = glob.glob(os.path.join(BASE_DIR,'*-L.txt'))	

	for x in dataList:
		base = os.path.basename(x)
		channel = os.path.splitext(base)[0]
		channel = channel.split('_')[0]
		if channel == "N+N":
			channel = "N-N"

		#Retrieve data from source and build payload from file
		payload = getKeyPayload(x,channel)

		# Send try sending to Ubidots if there is data in payload
		if payload:
			post_var(payload,"industrial.api.ubidots.com",device,token)
		else:
			print("No data for channel {}.".format(channel))
	print("Run finished at {}.".format(datetime.now()))
	
if __name__ == "__main__":
	main()
