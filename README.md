# ISP-Speedtest
python3 script to keep an eye on the speed that a (my) ISP provides

It works with the Ookla Cli for linux https://www.speedtest.net/apps/cli, print the results in a influxDB https://www.influxdata.com/ which i monitor with a Grafana Backend https://grafana.com/ .

It is triggert by a crontab like:
*/30    *       *       *       *       python3         speedTest.py
so every 30 minutes is this script triggert what will couse about 48 unic mesuremnts per day.


To get more valid and scattered results the scripts generates a random wait counter between 0 sec and 30 mins.

WIP:
Creat a bash file that install and set up the speedtest from ookla , python3 with required packages, influx and grafana.
