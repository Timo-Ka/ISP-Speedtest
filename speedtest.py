# this Code is writen under MIT License

# Copyright (c) 2021 Tim Hansmeyer

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from datetime import datetime
from dotenv import load_dotenv
from influxdb import InfluxDBClient
import os
import random
import re
import subprocess
import sys
import time

# "GLOBAL VARS"
# debug ist used to print out lines that will overview the status of the script

load_dotenv()

debug = False
if len(sys.argv) == 2:
    if sys.argv[1] == "debug":
        debug = True
        print("DEBUG IT!")

# Logfile where the status will be write to if needed
logFilePathAndName = 'speedteststatus.txt'
logErrorFilePathAndName = 'speedtestFails.txt'


config = {
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASS'),
        'host': os.getenv('DB_HOST'),
        'database': os.getenv('DB_NAME')
    }

# Helper functions:
# ping googel (or whatever) to check it the internet connection exists
def pingToCheckTheInternetConnection(host = os.getenv('PING_TARGET')):
    if debug:
        print('running ping Function - function name : pingToCheckTheInternetConnection')
        
    hostnameToPing = host
    responsePing = os.system("ping -c 1 " + hostnameToPing)

    if responsePing == 0:
        responsePingAsString = True
        if debug:
            print('pinging google sucsessfully')
        else:
            print('pinging google failed, prply no ')
    else:
        responsePingAsString = False
    
    return responsePingAsString
# End

# Write status in file
def writeStatusInFile(fileNameWithPath, textToInputInTheFile, writeBehavior = "a+" ):
    
    if debug:
        print('running write to file function - function name : writeStatusInFile')
    
    dateTimeObjInWriteStatusInFile = str(datetime.now())
    
    try:
        file = open(fileNameWithPath, writeBehavior)
        file.write(dateTimeObjInWriteStatusInFile)
        file.write('\n ')
        file.write(str(textToInputInTheFile))
        file.write('\n ')
        file.close()
        if debug:
            print('writing it down sucessfully')
        return True

    except Exception as e:
        if debug:
            print('Writer chrashed  / Somthing ugly happend')
        pass
        if debug:
            print('writing that error back to file')
        errorFile = open(logErrorFilePathAndName, 'a+')
        errorFile.write(dateTimeObjInWriteStatusInFile)
        errorFile.write('\n ')
        errorFile.write(str(e))
        errorFile.write('\n ')
        errorFile.close()
        quit()
        return False
        # TODO wite a mail that something crashed 
# End

# generate a Random Int wich is needet in some cases
def generateRandomInt(min = 0, max = 1):
    return random.randint(min,max)
# End

# runns the speedtest as cli tool from ookla
def speedtest(serverselector):
    if serverselector == 1:
        return subprocess.Popen('speedtest -s 29320', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    else:
        return subprocess.Popen('speedtest', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
# End

# search and extract the values from the cli text
def extractFromResult(serachString, cliText):
    serachString = str(serachString)
    serachString = serachString + ':\s+(.*?)\s'
    serachStringRegex = re.search(serachString, cliText, re.MULTILINE)
    serachedString = serachStringRegex.group(1)
    if debug:
        print("serachString " + serachedString)
    return serachedString
# End



# decides if the speedtest runs against a specific Server. 1 maeans Witcom in Wiesbaden, Server number 29320, a 0 means we choose a random one
# this is because witcome is the closest to my location but i dont wana wast measuments if witcom would break, have tecnical problems or stop the service
selectServerForSpeedTest = generateRandomInt()
if debug:
    print("selectServerForSpeedTest " + str(selectServerForSpeedTest))

# create a random delay up to 30 mins before the check starts
waitingTimeInSeconds = generateRandomInt(0,1800)
if debug:
    print('waitingTimeInSeconds was definded from randum number generator as - ', waitingTimeInSeconds, ' - ')
    waitingTimeInSeconds = 0
    print('waitingTimeInSeconds was hardcoded to - ', waitingTimeInSeconds, ' - for debugging reasons')

# Log the run of this script to a file
waitingTimeInSecondsAsString = str(waitingTimeInSeconds)
writeStatusInFile(logFilePathAndName,waitingTimeInSecondsAsString)

try:
    time.sleep(waitingTimeInSeconds)
    if debug:
        print("Printed after " + str(waitingTimeInSeconds) + " seconds.")
except Exception as e:
    writeStatusInFile(logErrorFilePathAndName, e)
    quit()

# define a counter for max retrys
offlineCounter = 0
offlineCounterMax = 3

while True:
    try:
        speedtestResult = speedtest(selectServerForSpeedTest)
        if debug:
            print("try speedtest")
    except Exception as e:
        writeStatusInFile(logErrorFilePathAndName, e)

    ping = extractFromResult('Latency', speedtestResult)
    download = extractFromResult('Download', speedtestResult)
    upload = extractFromResult('Upload', speedtestResult)
    url = extractFromResult('Result URL', speedtestResult)
    packetLoss  = extractFromResult('Packet Loss', speedtestResult)

    try:
        float(download)
        if debug:
            print('donwload ist a float')
    except Exception as e:
        writeStatusInFile(logErrorFilePathAndName, e)
        download = 0
        if debug:
            print('download is not a float, therfor its hardcoded to - ', download, ' - ')
    try:
        float(upload)
        if debug:
            print('upload ist a float')
    except Exception as e:
        writeStatusInFile(logErrorFilePathAndName, e)
        upload = 0
        if debug:
            print('upload is not a float, therfor its hardcoded to - ', upload, ' - ')
    try:
        float(ping)
        if debug:
            print('ping ist a float')
    except Exception as e:
        writeStatusInFile(logErrorFilePathAndName, e)
        ping = 999
        if debug:
            print('ping is not a float, therfor its hardcoded to - ', ping, ' - ')
    try:
        str(url)
        if debug:
            print('resultUrl ist a string')
    except Exception as e:
        writeStatusInFile(logErrorFilePathAndName, e)
        url = ""
        if debug:
            print('resultUrl is not a string, therfor its hardcoded to - ', url, ' - ')

    packetLoss = re.search('(\d){1,3}(\.)(\d){1,3}', packetLoss )
    if packetLoss:
        packetLoss = packetLoss.group(1) + packetLoss.group(2) + packetLoss.group(3)
        if debug:
            print("ping correctly build " + packetLoss)
    try:
        float(packetLoss)
        if debug:
            print('----packetloss ist a float------')
    except Exception as e:
        writeStatusInFile(logErrorFilePathAndName, e)
        packetLoss = -1
        if debug:
            print('-----packetloss is not a float, therfor its hardcoded to - ', packetLoss, ' - ')        

    if debug:
        print("---while---")

    # check the stats of DOWNLOAD - UPLOAD - URL - PACKETLOSS -> if they are ok exit the loop 
    variableStatus = []
    if download != 0:
        variableStatus.append(True)
        if debug:
            print("Download OK")
    else:
        variableStatus.append(False)

    if upload != 0:
        variableStatus.append(True)
        if debug:
            print("Upload OK")
    else:
        variableStatus.append(False)
            
    if url != "-":
        variableStatus.append(True)
        if debug:
            print("URL OK")
    else:
        variableStatus.append(False)
        
    if packetLoss != -1:
        #variableStatus.append(True)
        if debug:    
            print("packetLoss OK")
    #else:
        #variableStatus.append(False)
    
    if all(variableStatus):
        break    
    else:
        if debug:
            print('Check if pi is connectet to the internet')
        if offlineCounter == offlineCounterMax:
            if debug:
                print('-- 3trd try jumping out, not connect with the internet -- ')

            isInternetConnected = pingToCheckTheInternetConnection()
            if not isInternetConnected:
                download = 0
                upload = 0
                ping = 999
                url = "-"
                packetLoss = 99
                break
            else:
                speedtestFails3rdTime = "looks like the speedtest fails 3 times... Sys-Ad plz check"
                writeStatusInFile(logErrorFilePathAndName, speedtestFails3rdTime)
                break

        offlineCounter += 1

if debug:
    print("DATA IS VALID")

speed_data = [
    {
        "measurement" : "networkSpeed",
        "tags" : {
            "host": "DietPi"
        },
        "fields" : {
            "download": float(download),
            "upload": float(upload),
            "ping": float(ping),
            "URL": url,
            "packetLoss": float(packetLoss)
        }
    }
]

if debug:
    print("pump data in db ")

client = InfluxDBClient(config["host"], 8086, config["user"], config["password"], config["database"])
try:
    client.write_points(speed_data)
    if debug:
        print("DATA WAS TASTY - IM DONE")
except Exception as e:
    writeStatusInFile(logErrorFilePathAndName, e)
    if debug:
        print("FFS something happend check your log")
