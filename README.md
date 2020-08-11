# py-owm-mqtt

Python script to push OpenWeatherMap temp information (temperature, feels-like-temp, and humidity) to my local mqtt

# Setup
## Config File

Modify *config.cfg.example* and rename as *config.cfg*.  Include the following parameters:

	[mqtt]
	ipaddr = 'yourMqttServerIP'
	port = 1883
	topic = 'yourMqtt/tokenName/here'

	[owm]
	token = 'yourTokenHere'
	USzipcode = 'yourZipCode'
Mqtt parameters should be self explanatory, Owm token comes from OpenWeatherMap's api

This file is copied into the docker container on build, so it is required to be configured.

## Testing Python Script locally

Temporarily create local folder 'log' for the script to store files in 

After updating config.cfg file, run the *py-owm-mqtt.py* script

    python py-owm-mqtt.py

On first run you will need to authorize app with ecobee.com in the My Apps section. Follow instructions, this will make a persistent database file in ./db folder created above.

# Docker
I did this development on a Windows machine in Git Bash, so a couple of these commands might be a little wonky...
## Build the docker file

    docker build -t py-owm-mqtt .

Response:

    Sending build context to Docker daemon  1.313MB
	Step 1/7 : FROM python:3.8
	 ---> 6feb119dd186
	Step 2/7 : copy config.cfg /app/config.cfg
	 ---> Using cache
	 ---> 2cdbeca4129b
	Step 3/7 : copy py-owm-mqtt.py /app/py-owm-mqtt.py
	 ---> 6ce88da4f374
	Step 4/7 : copy requirements.txt /app/requirements.txt
	 ---> a1541a0b534b
	Step 5/7 : RUN mkdir /app/log
	 ---> Running in 571c76f352bb
	Removing intermediate container 571c76f352bb
	 ---> 45a69bd38d99
	Step 6/7 : RUN pip install -r /app/requirements.txt
	 ---> Running in ea996deeaa04
	Collecting requests
	  Downloading requests-2.24.0-py2.py3-none-any.whl (61 kB)
	Collecting configparser
	  Downloading configparser-5.0.0-py3-none-any.whl (22 kB)
	Collecting paho-mqtt
	  Downloading paho-mqtt-1.5.0.tar.gz (99 kB)
	Collecting pyowm
	  Downloading pyowm-3.0.0-py3-none-any.whl (3.3 MB)
	Collecting chardet<4,>=3.0.2
	  Downloading chardet-3.0.4-py2.py3-none-any.whl (133 kB)
	Collecting urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1
	  Downloading urllib3-1.25.10-py2.py3-none-any.whl (127 kB)
	Collecting idna<3,>=2.5
	  Downloading idna-2.10-py2.py3-none-any.whl (58 kB)
	Collecting certifi>=2017.4.17
	  Downloading certifi-2020.6.20-py2.py3-none-any.whl (156 kB)
	Collecting PySocks<2,==1.7.1
	  Downloading PySocks-1.7.1-py3-none-any.whl (16 kB)
	Collecting geojson<3,>=2.3.0
	  Downloading geojson-2.5.0-py2.py3-none-any.whl (14 kB)
	Building wheels for collected packages: paho-mqtt
	  Building wheel for paho-mqtt (setup.py): started
	  Building wheel for paho-mqtt (setup.py): finished with status 'done'
	  Created wheel for paho-mqtt: filename=paho_mqtt-1.5.0-py3-none-any.whl size=61415 sha256=3a713712b934394ae3025179bb497d1a697a78a31c45ac74f06a1d59d456697f
	  Stored in directory: /root/.cache/pip/wheels/c6/63/e1/6e3a42c72eb48428f83a5718662fc2273b0ffe7f644085cc4e
	Successfully built paho-mqtt
	Installing collected packages: chardet, urllib3, idna, certifi, requests, configparser, paho-mqtt, PySocks, geojson, pyowm
	Successfully installed PySocks-1.7.1 certifi-2020.6.20 chardet-3.0.4 configparser-5.0.0 geojson-2.5.0 idna-2.10 paho-mqtt-1.5.0 pyowm-3.0.0 requests-2.24.0 urllib3-1.25.10
	Removing intermediate container ea996deeaa04
	 ---> 802d5daf4323
	Step 7/7 : CMD ["python", "/app/py-owm-mqtt.py"]
	 ---> Running in 7e7a7d21a525
	Removing intermediate container 7e7a7d21a525
	 ---> d3fe3e945e2d
	Successfully built d3fe3e945e2d
	Successfully tagged py-owm-mqtt:latest
	SECURITY WARNING: You are building a Docker image from Windows against a non-Windows Docker host. All files and directories added to build context will have '-rwxr-xr-x' permissions. It is recommended to double check and reset permissions for sensitive files and directories.





## First time executing!

     winpty docker run -it -v "C:\Users\derek.ROWKAR\Documents\repos\py-owm-mqtt\log-docker":/app/log -name py-owm-mqtt py-owm-mqtt
winpty - Git Bash isn't a tty client, so can't use interactive mode, winpty lets us interact with docker run command

 - *winpty* : Git Bash isn't a tty client, so can't use interactive mode,
   winpty lets us interact with docker run command
 - *docker run -it* : run the docker container in interactive and tty modes so we can authorize app if needed
 - *-v [local folder]:/app/log* : maps docker's log folder to a folder on your local PC so you can checkout logs
 - *py-owm-mqtt* : this is the name of the container built above
 
To exit, hit CTRL+C and container should continue running

### Run detached

Add "-d" to command above once it's running

     
