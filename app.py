#!/usr/bin/env python

import sys
import os
from bottle import route, run, static_file, template, view, post, get
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
import time
import gevent
import HardwareInterface as hw
import picamera
myQ = []

def notify_click():
    print "Click"
    for u in users:
        u.send("feed us!!!")

    #myQ.append("CLICK CLICK")

myhw = hw.HardwareInterface()
myhw.on_button_up(notify_click)
myhw.start()

@route('/js/<filename>')
def js_static(filename):
    return static_file(filename, root='./js')

@route('/img/<filename>')
def img_static(filename):
    return static_file(filename, root='./img')

@route('/css/<filename>')
def img_static(filename):
    return static_file(filename, root='./css')


@post("/merp")
def merp():
    myhw.power_down()
    myhw.join()


@post("/buzz")
def buzz():
    myhw.buzz_once()
    for u in users:
        u.send("buzz")

@post("/feed")
def dispense():
    myhw.dispense()
    for u in users:
        u.send("feed")


@route("/pics")
@view("live")
def live():
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        #camera.start_preview()
        # Camera warm-up time
        time.sleep(0.5)
        camera.capture('img/live.jpg')
    return dict(title = "Hello", button="derp2", content = '''
    Hello from Python!

    ''')


@route("/")
@view("main")
def hello():
    return dict(title = "Hello", button="derp2", content = '''
    Hello from Python!

    ''')

users = set()
@get('/websocket', apply=[websocket])
def chat(ws):
    users.add(ws)
    while True:
        msg = ws.receive()
        print msg
        if msg is not None:
            for u in users:
                u.send(msg)
        else: 
            break
    users.remove(ws)    


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    run(host='192.168.1.42', port=port, server=GeventWebSocketServer)
     

