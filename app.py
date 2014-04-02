#!/usr/bin/env python

import sys
import os
from bottle import route, run, static_file, template, view, post, get
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
import time
import gevent
import HardwareInterface as hw
myQ = []

def notify_click():
    print "Click"
    for u in users:
        u.send("CLICK CLICK")

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


@route("/merp")
@view("main")
def merp():
    return dict(title="MERP",content="MERP!")


@post("/derp")
def derp():
    myhw.buzz_once()
    for u in users:
        u.send("DERP DERP DERP")
    print "DERP DERP DERP"
    myhw.power_down()
    myhw.join()

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
     

