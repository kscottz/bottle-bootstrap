#!/usr/bin/env python

import os
from bottle import route, run, static_file, template, view, post

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
    print "DERP DERP DERP"

@route("/")
@view("main")
def hello():
    return dict(title = "Hello", button="derp2", content = '''
    Hello from Python!

    ''')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    run(host='0.0.0.0', port=port)
