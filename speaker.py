# -*- coding: utf-8 -*-

import base64
import json
import os
import sys
import time

import pyaudio
import paho.mqtt.subscribe as subscribe

HOST = os.environ.get("HOST", "localhost")
TENANT = os.environ.get("TENANT", "admin")
DEVICE = os.environ.get("DEVICE")
RATE = int(os.environ.get("RATE", "16000"))
CHANNELS = int(os.environ.get("CHANNELS", "1"))

pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16,
                 channels=CHANNELS, rate=RATE,
                 output=True)


def play(audio):
    global stream
    audio = base64.b64decode(audio)
    stream.write(audio)


def on_message_config(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode("utf8"))
        attrs = payload.get("attrs")
        if isinstance(attrs, dict):
            play(attrs.get("audio"))
    except Exception as e:
        print(str(e))
        sys.stdout.flush()


subscribe.callback(on_message_config, "/%s/%s/config" % (TENANT, DEVICE), hostname=HOST, port=1883, 
                   client_id=TENANT + ":" + DEVICE, auth={"username": TENANT, "password": DEVICE})

while True:
    time.sleep(0.1)

stream.stop_stream()
stream.close()
pa.terminate()
