#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    File name: py-owm-mqtt.py
    Author: Derek Rowland
    Date created: 2020/08/07
    Date last modified: 2020/08/07
    Python Version: 3.8.5
'''

'''
******* Imports 
'''
import requests
import os, sys, signal, time
from configparser import ConfigParser
import paho.mqtt.client as mqtt
import pyowm

from datetime import datetime

import pytz
from six.moves import input

import json

import logging
from logging.handlers import TimedRotatingFileHandler

'''
******* Header Vars
'''

__author__ = "Derek Rowland"
__copyright__ = "Copyright 2020"
__credits__ = ["Derek Rowland"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Derek Rowland"
__email__ = "gx1400@gmail.com"
__status__ = "Development"

'''
******* Global vars
'''
logger = logging.getLogger(__name__)
mqttAddr = 'not loaded'
mqttPort = -1
mqttTopic = 'not loaded'
tokenOwm = 'not loaded'
owm = None
terminate = False
client = None
location = ''

'''
******* Functions
'''
def main():
    global client

    # Read Config File parameters
    read_config()

    logger_setup()

    #try to connect to ecobee
    owm_setupAPI()
    
    # Connect to Mqtt
    client = mqtt.Client()
    client.on_connect = mqtt_on_connect
    client.on_message = mqtt_on_message
    
    try:
        logger.info('Attempting to connect to mqtt server: ' + mqttAddr + 
            ':' + str(mqttPort))
        client.connect(mqttAddr, mqttPort, 60)
    except:
        logger.error('failed to connect to mqtt.... aborting script')
        sys.exit()
    
    signal.signal(signal.SIGINT, signal_handler)
    logger.info('Starting loop...')

    client.loop_start()
    loopct = 0

    try:
        while True:
            if terminate:
                mqtt_endloop()
                break
        
            if (loopct >= 60):
                logger.info('Start of loop')
                try:
                    owm_getWeather(location)
                except requests.ConnectionError:
                    logger.error('Connection error!')
                except requests.Timeout:
                    logger.error('Timeout error')
                except requests.RequestException as e:
                    raise SystemExit(e)
                loopct = 0
            else:
                time.sleep(1)
                loopct += 1
    except:
        logger.error("Unexpected error:", sys.exc_info()[0])
        
    
    logger.info('Exiting program')

def donothing():
    nothing = None   

def logger_setup():
    global logger
    thisfolder = os.path.dirname(os.path.abspath(__file__))
    logFile = os.path.join(thisfolder, 'log', 'logger.log')

    formatter = logging.Formatter('%(asctime)s %(name)-18s %(levelname)-8s %(message)s')
    handler = TimedRotatingFileHandler(logFile,
                                       when="d",
                                       interval=1,
                                       backupCount=7)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    logger.setLevel(logging.DEBUG)

def mqtt_endloop():
    client.loop_stop()
    logger.info('loop stopped!')
    client.disconnect()

# call back for client connection to mqtt
def mqtt_on_connect(client, userdata, flags, rc):
    logger.info('Mqtt Connection result code: ' + str(rc))

    # subscribing in on_connect means if we lose the connection and 
    # reconnect then subscriptions will be renewed
    client.subscribe('$SYS/#')
    

# call back for when a public message is received by the server
def mqtt_on_message(client, userdata, msg):
    donothing()

def owm_setupAPI():
    print('try to auth with omw')
    global owm
    owm = pyowm.OWM(tokenOwm)

def owm_getWeather(loc):
    try:
        mgr = owm.weather_manager()
        print(loc)
        observation = mgr.weather_at_zip_code(loc,'US')
        w = observation.weather
        print('got weather')
        temp = str(w.temperature('fahrenheit')['temp'])
        feelslike = str(w.temperature('fahrenheit')['feels_like'])
        hum = str(w.to_dict()['humidity'])

        print('topic: ' + mqttTopic)
        msg = {
            'temp': temp,
            'feelslike': feelslike,
            'humidity': hum
        }
        print('topic: ' + mqttTopic + ', msg: ' + json.dumps(msg))
        client.publish(mqttTopic, json.dumps(msg), 0, False)

    except:
        logger.error('error getting weather info')

# function for reading the config.cfg file to set global operation params
def read_config():
    parser = ConfigParser()
    thisfolder = os.path.dirname(os.path.abspath(__file__))
    configfile = os.path.join(thisfolder, 'config.cfg')
    parser.read(configfile, encoding=None)

    global mqttAddr, mqttPort, mqttTopic, tokenOwm, location

    mqttAddr = parser.get('mqtt', 'ipaddr').strip('\'')
    mqttPort = parser.getint('mqtt', 'port')
    mqttTopic = parser.get('mqtt', 'topic').strip('\'')

    tokenOwm = parser.get('owm', 'token').strip('\'')
    location = parser.get('owm', 'USzipcode').strip('\'')
    print()

def signal_handler(signum,frame):
    global terminate
    terminate = True

# main function call
if __name__ == "__main__":
    main()