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
Crontab command
*/30 * * * * /usr/bin/python2.7 /home/pi/ComScriptPi/profiles/NuLAB_Logging/ubidots_upload.py >> /home/pi/ComScriptPi/profiles/NuLAB_Logging/ubidots.log 2>&1
'''

'''
global variables
'''
BASE_DIR=os.path.dirname(os.path.realpath(__file__))
#FolderName = ''			#Use if placed in folder above data.  
ENDPOINT = "industrial.api.ubidots.com"
device = "#######_nulab"
token = "BBFF-3SW5GCgLEF4DVUpYRNMylqFyXAFUDA"	#LTI Token
buoyDateFormat = '%m/%d/%Y %H:%M:%S'

def get_valueSentCheck(variable,dateTime):
		
	dctData = {}
	#If file does not exist then create file and add param and time.
	if os.path.isfile("ubidots_lastSend.json"):
		f = open("ubidots_lastSend.json","r")
		#If error then file exists but is empty. Create variable key and assign 0 time. 
		try:		
			dctData = json.load(f)
			
		except Exception:
			dctData = {}
			dctData[variable] = 0
		f.close()
		#Check if param exists. No add it to dict. Yes extract time and check if new.
		if variable in dctData:
			lastValueSentTime = dctData[variable]
			if (dateTime == lastValueSentTime):
				print("Station {} value {} has already been sent.".format(device,variable))
				sent = True
			else:
				print("Station {} value {} has not been sent. Adding to payload".format(device,variable))
				dctData[variable] = dateTime
				sent = False
		else:
			dctData[variable] = dateTime
			print("Station {} value {} has not been sent. Adding to payload".format(device,variable))		
			sent = False
	else:
		dctData = {variable:dateTime}
		sent = False
		
	#Write out dict whether or not modified		
	f2 = open('ubidots_lastSend.json','w+')	
	f2.write(json.dumps(dctData, indent=1))
	f2.close()
	return sent
		
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
	
	#Dissolved and total chemistry has different headers
	try:
		OBSabsLoc = variables.index("OBS_abs")
		OBSconcLoc = variables.index("OBS_conc")
		SmpabsLoc = variables.index("Smp_abs")
		SmpconcLoc = variables.index("Smp_conc")
	except:
		try:
			TN_SmpabsLoc = variables.index("TN_Smp_Abs")
			TN_SmpconcLoc = variables.index("TN_Smp_Conc")
		except:
			TP_SmpconcLoc = variables.index("TP_Smp_Conc")
			TP_SmpabsLoc = variables.index("TP_Smp_Abs")
	macro1 = []
	macro1_ref = []	#Extract for ref light
	macro2 = []
	macro2_ref = []	#Extract for ref light
	macro8 = []
	#Reverse lines so the newest data will appear first in array	
	for d in reversed(lines):
		#Will fail for lines were array location does not exist		
		try:
			data = d.strip().split(",")
			if data[macroLoc] == "M1" and data[SmpconcLoc]:
				macro1.append(data)
			elif data[macroLoc] == "M2" and data[OBSconcLoc]:
				macro2.append(data)
			elif data[macroLoc] == "M8" and data[15]:
				if not "CalMode" in data[4]:
					macro8.append(data)
					
		except:
			#Try to extract macros for ref light
			try:		
				if data[macroLoc] == "M1":
					macro1_ref.append(data)
				elif data[macroLoc] == "M2":
					macro2_ref.append(data)
			except:
				pass
	#Check for empty data for macro1 or macro2 results. If empty then return empty payload
	if not (macro1 or macro2 or macro8):
		return payload
	#Create Unix time in milliseconds from first timestamp always located in first array location
	SmpTimestamp = []
	ObsTimestamp = []
	try:
		SmpDateTime = datetime.strptime(macro1[0][0],buoyDateFormat)	
		SmpTimestamp = ((SmpDateTime - datetime(1970,1,1)).total_seconds())*1000
		ObsDateTime = datetime.strptime(macro2[0][0],buoyDateFormat)	
		ObsTimestamp = ((ObsDateTime - datetime(1970,1,1)).total_seconds())*1000
	except:
		SmpDateTime = datetime.strptime(macro8[0][0],buoyDateFormat)	
		SmpTimestamp = ((SmpDateTime - datetime(1970,1,1)).total_seconds())*1000
	for x in range(len(variables)):
		if variables[x] in ['OBS_abs','OBS_conc']:
			dateTime = ObsTimestamp
			dataSend = macro2
		elif variables[x] in ['Smp_abs','Smp_conc']:
			dateTime = SmpTimestamp
			dataSend = macro1
		elif variables[x] in ['TP_Smp_Abs','TN_Smp_Abs','TP_Smp_Conc','TN_Smp_Conc']:
			#Remove TN_/TP_ from variable name
			variables[x] = variables[x].split('_',1)[1]
			dateTime = SmpTimestamp
			dataSend = macro8
		#Case if parmater is used in both OBS and Sample 
		elif variables[x] in ['Light']:
			paramName1 = channel+"-Smp_"+variables[x]
			paramName2 = channel+"-OBS_"+variables[x]
			updateValue1 = get_valueSentCheck(paramName1, SmpTimestamp)
			if (updateValue1 is False):
				#NaN's will cause error. Pass sending variable. 
				try:
					value = float(macro1[0][x])
					payload[paramName1] ={'value':value,'timestamp':SmpTimestamp}
					#Send ref light also
					paramName1 = paramName1 + "_Ref"
					value2 = float(macro1_ref[0][x])
					payload[paramName1] ={'value':value2,'timestamp':SmpTimestamp}
				except:
					try:			
						value = float(macro8[0][x])
						payload[paramName1] = {'value':value,'timestamp':SmpTimestamp}
					except:
						continue
			#Only check if there is an OBS 			
			if (ObsTimestamp):
				updateValue2 = get_valueSentCheck(paramName2, ObsTimestamp)
				if (updateValue2 is False):
					#NaN's will cause error. Pass sending variable. 
					try:
						value = float(macro2[0][x])
						payload[paramName2] ={'value':value,'timestamp':ObsTimestamp}
						#Send ref light also
						paramName2 = paramName2 + "_Ref"
						value2 = float(macro2_ref[0][x])
						payload[paramName2] ={'value':value2,'timestamp':SmpTimestamp}
					except:
						continue
				#Skip to next variable
				continue
			else:
				continue
		else:
			continue
		paramName = channel+"-"+variables[x]
		
		updateValue = get_valueSentCheck(paramName, dateTime)
		if (updateValue is False):
			#NaN's will cause error. Pass sending variable. 
			try:
				value = float(dataSend[0][x])
				payload[paramName] ={'value':value,'timestamp':dateTime}
			except:
				continue
	return payload
	
def post_var(payload, url, device, token):

	try:
		url = "http://{}/api/v1.6/devices/{}".format(url, device)
		headers = {"X-Auth-Token": token, "Content-Type": "application/json"}
		attempts = 0
		status_code = 400
		while status_code >= 400 and attempts < 2:
			print("[INFO] Sending data, attempt number: {}".format(attempts))
			req = requests.post(url=url, headers=headers,data=json.dumps(payload))
			status_code = req.status_code
			attempts += 1
			time.sleep(10)
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
	payload = {}	
	for x in dataList:
		base = os.path.basename(x)
		channel = os.path.splitext(base)[0]
		channel = channel.split('_')[0]
		if channel == "N+N":
			channel = "N-N"
		print(channel)
		#Retrieve data from source and build payload from file
		payload_param = getKeyPayload(x,channel)
		if payload_param:
			payload.update(payload_param)

	# Send try sending to Ubidots if there is data in payload
	if payload:
		post_var(payload,ENDPOINT,device,token)
		print(payload)
	else:
		print("No data for channel {}.".format(channel))
	
	print("Run finished at {}.".format(datetime.now()))
	
if __name__ == "__main__":
	main()
