# -*- coding: utf-8 -*-

import base64
import json
import os
import sys
import time

import pyaudio
import paho.mqtt.subscribe as subscribe

HOST = os.environ.get("HOST")
TENANT = os.environ.get("TENANT")
DEVICE = os.environ.get("DEVICE")
RATE = int(os.environ.get("RATE"))
CHANNELS = int(os.environ.get("CHANNELS"))

pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16,
                 channels=CHANNELS, rate=RATE,
                 output=True)


def play(audio):
    global stream
    audio = base64.b64decode(audio)
    stream.write(audio)


def on_camera_config(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode("utf8"))
        attrs = payload.get("attrs")
        if isinstance(attrs, dict):
            play(attrs.get("audio"))
    except Exception as e:
        print(str(e))
        sys.stdout.flush()


subscribe.callback(on_camera_config, "/%s/%s/attrs" % (TENANT, DEVICE), hostname=HOST, port=1883)

while True:
    time.sleep(1)
