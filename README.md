# ISP-Speedtest
python3 script to keep an eye on the speed that a (my) ISP provides

It works with the Ookla Cli for linux https://www.speedtest.net/apps/cli, print the results in a influxDB https://www.influxdata.com/ which i monitor with a Grafana Backend https://grafana.com/ .

To get this script running you have to install:
ookla speedtest cli 
influxdb
grafana &
python3 with these packages
  > from datetime import datetime
  > from dotenv import load_dotenv
  > from influxdb import InfluxDBClient
  > import os
  > import random
  > import re
  > import subprocess
  > import sys
  > import time

The accsses to the database is configured in the .env file, please rename the including example.env and modify it.


A crontab to trigger this script every 30 mins looks like this

*/30    *       *       *       *       python3         (insert/Your/Path/Here/)speedtest.py

so every 30 minutes is this script triggert what will couse about 48 unic mesuremnts per day.


To get more valid and scattered results the scripts generates a random wait counter between 0 sec and 30 mins.

WIP:
Creat a bash file that install and set up the speedtest from ookla , python3 with required packages, influx and grafana.
