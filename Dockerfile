FROM python:3.8
copy config.cfg /app/config.cfg
copy py-owm-mqtt.py /app/py-owm-mqtt.py
copy requirements.txt /app/requirements.txt
RUN mkdir /app/log
RUN pip install -r /app/requirements.txt
CMD ["python", "/app/py-owm-mqtt.py"]