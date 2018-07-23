# -*- coding: utf-8 -*-

import base64
import json
import os
import sys
import time

import cv2
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe

HOST = os.environ.get("HOST", "localhost")
TENANT = os.environ.get("TENANT", "admin")
DEVICE = os.environ.get("DEVICE")
WIDTH = int(os.environ.get("WIDTH", "640"))
HEIGHT = int(os.environ.get("HEIGHT", "480"))
FPS = float(os.environ.get("FPS", "25"))
capture = None


def record():
    global capture
    capture = cv2.VideoCapture(0)
    capture.set(3, WIDTH)
    capture.set(4, HEIGHT)
    capture.set(5, FPS)
    while capture is not None and capture.isOpened():
        ret, frame = capture.read()
        if ret == True:
            retval, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
            image = base64.b64encode(buffer).decode("utf8")
            payload = json.dumps({"frame": image})
            publish.single("/%s/%s/attrs" % (TENANT, DEVICE), payload, hostname=HOST)


def stop():
    global capture
    if capture is not None:
        capture.release()


def on_message_config(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode("utf8"))
        attrs = payload.get("attrs")
        if attrs.get("action") == "record":
            record()
        elif attrs.get("action") == "stop":
            stop()
    except Exception as e:
        print(str(e))
        sys.stdout.flush()


subscribe.callback(on_message_config, "/%s/%s/config" % (TENANT, DEVICE), hostname=HOST, 
                   client_id=TENANT + ":" + DEVICE, auth={"username": TENANT, "password": DEVICE})

while True:
    time.sleep(0.1)

