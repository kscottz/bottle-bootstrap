#!/usr/bin/env python



import sys
#if 'threading' in sys.modules:
#        raise Exception('threading module loaded before patching!')
#from gevent import monkey; monkey.patch_all(), sleep
#import gevent
#from gevent import monkey; monkey.patch_all()
import os
#import threading
#import time
from bottle import route, run, static_file, template, view, post, get
#import gevent
#from gevent import pywsgi
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
import time
import gevent

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
    for u in users:
        u.send("DERP DERP DERP")
    print "DERP DERP DERP"

@route("/")
@view("main")
def hello():
    return dict(title = "Hello", button="derp2", content = '''
    Hello from Python!

    ''')

# @route('/stream')
# def stream():
#     count = 0
#     while True:
#         count = count + 1
#         print count
#         gevent.sleep(0.1)
#         yield "t={0}".format(count)
#     time.sleep(1)
#     yield 'MIDDLE'
#     time.sleep(1)
#     yield 'END'

# from gevent import monkey
# monkey.patch_all()

# import datetime
# import time
# from gevent import Greenlet
# from gevent import pywsgi
# from gevent import queue


# def current_time(body):
#     current = start = datetime.datetime.now()
#     end = start + datetime.timedelta(seconds=60)

#     while current < end:
#         current = datetime.datetime.now()
#         body.put('<div>%s</div>' % current.strftime("%Y-%m-%d %I:%M:%S"))
#         time.sleep(1)

#     body.put('</body></html>')
#     body.put(StopIteration)

# @route("/")
# #@view("main")
# def handle()#environ, start_response):
#     start_response('200 OK', [('Content-Type', 'text/html')])
#     body = queue.Queue()
#     body.put(' ' * 1000)
#     body.put("<html><body><h1>Current Time:</h1>")
#     g = Greenlet.spawn(current_time, body)
#     return body
users = set()
@get('/websocket', apply=[websocket])
def chat(ws):
    users.add(ws)
    while True:
        msg = ws.receive()
        #msg = "herp : derp"
        print msg
        if msg is not None:
            for u in users:
                u.send(msg)
            t#ime.sleep(0.1)
        else: break
    users.remove(ws)    


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    #server = pywsgi.WSGIServer(('127.0.0.1', port), handle)
    run(host='0.0.0.0', port=port, server=GeventWebSocketServer)
    #print "Serving on http://127.0.0.1:5000..."
    #server.serve_forever()
    

