# -*- coding: utf-8 -*-

import base64
import json
import os
import time
import wave

import pyaudio
import paho.mqtt.publish as publish

HOST = os.environ.get("HOST")
TENANT = os.environ.get("TENANT")
DEVICE = os.environ.get("DEVICE")
RATE = int(os.environ.get("RATE"))
CHANNELS = int(os.environ.get("CHANNELS"))


def on_stream(in_data, frame_count, time_info, status_flags):
    audio = base64.b64encode(in_data).decode("utf8")
    payload = json.dumps({"audio": audio})
    publish.single("/%s/%s/attrs" % (TENANT, DEVICE), payload, hostname=HOST)
    return None, pyaudio.paContinue


pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16,
                 channels=CHANNELS, rate=RATE,
                 input=True, frames_per_buffer=int(RATE / 5),
                 stream_callback=on_stream)
stream.start_stream()

while stream.is_active():
   time.sleep(0.1)

stream.stop_stream()
stream.close()
pa.terminate()
