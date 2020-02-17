#!/usr/bin/env python3

from flask import Flask, render_template, abort, request, url_for, redirect, request, jsonify, flash, session, g, json
import re
import os

import traceback

import socketio


import json

sio = socketio.Server(async_mode='threading')
app = Flask(__name__)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

# client = MongoClient('localhost', 27017)

# db = client['boojom']
# tags = db.tags
# objects = db.objects
# users = db.users

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

users = []

# @app.before_request
# def before_request():
# 	g.user = None
# 	if 'username' in session:
# 		g.user = users.find_one({'username': session['username']})

@app.route("/", methods=['POST', 'GET'])
def hello():
	return render_template('index.html', users=json.dumps(users))

@sio.event
def connect(sid, environ):
	print('connect: {}'.format(sid))
	users.append(sid)
	print('users: {}'.format(users))
	sio.emit('new_connection', {'userid': sid})

@sio.event
def disconnect(sid):
	print('disconnect: {}'.format(sid))
	users.remove(sid)
	print('users: {}'.format(users))
	sio.emit('new_disconnection', {'userid': sid})

@sio.event
def step(userid, to):
	print('step: {} to the {}'.format(userid, to))
	sio.emit('step', {'userid': userid, 'to': to})

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
#_____Auth/


"""
не пашит :-(
if app.debug:
	from flaskext.stylus2css import stylus2css
	stylus2css(app, css_folder='static/css', stylus_folder='stylus')
"""
