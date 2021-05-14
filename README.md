# ISP-Speedtest
python3 script to keep an eye on the speed that a (my) ISP provides

It works with the Ookla Cli for linux https://www.speedtest.net/apps/cli, print the results in a influxDB https://www.influxdata.com/ which i monitor with a Grafana Backend https://grafana.com/.
In the script included is a break condition. If the speedtest cant perform more then 3 times correct it will ping the PING_TARGET from the env to make sure you have a existing internet connection, if not the script will return the following to database:
<ul>
    <li>download = 0</li>
    <li>upload = 0</li>
    <li>ping = 999</li>
    <li>url = ""</li>
    <li>packetLoss = 99%</li>
</ul>

To get this script running you have to install:
<ul>
    <li>ookla speedtest cli</li>
    <li>influxdb</li>
    <li>grafana &</li>
    <li>python3 with these packages</li>
    <ul>
        <li>from datetime import datetime</li>
        <li>from dotenv import load_dotenv</li>
        <li>from influxdb import InfluxDBClient</li>
        <li>import os</li>
        <li>import random</li>
        <li>import re</li>
        <li>import subprocess</li>
        <li>import sys</li>
        <li>import time</li>
    </ul>
</ul>

The accsses to the database is configured in the .env file, please rename the including example.env and modify it.
In the 


A crontab to trigger this script every 30 mins looks like this

*/30    *       *       *       *       python3         (insert/Your/Path/Here/)speedtest.py

so every 30 minutes is this script triggert what will couse about 48 unic mesuremnts per day.


To get more valid and scattered results the scripts generates a random wait counter between 0 sec and 30 mins.

WIP:
Creat a bash file that install and set up the speedtest from ookla , python3 with required packages, influx and grafana.
