#!/usr/bin/env python
from bottle import get, post, run, redirect, request, default_app, static_file
import launch_nectar_instance
import os

@get('/')
def index():
  return static_file('index.html', '.')

@get('/main.js')
def index():
  return static_file('main.js', '.')

@get('/main.css')
def index():
  return static_file('main.css', '.')

@get('/logos/<filename>')
def index(filename):
  return static_file(filename, './logos')

@post('/launch')
def launch():
  username = request.params.get('username')
  pw = request.params.get('password')
  return launch_nectar_instance.launchFor(username, pw)

port = int(os.environ.get('PORT', 8080))

if __name__ == "__main__":
  try:
    try:
      run(host='0.0.0.0', port=port, debug=True, server='gunicorn', workers=8, reloader=True, timeout=1200)
    except ImportError:
      run(host='0.0.0.0', port=port, debug=True, reloader=True, timeout=1200)
  except Exception as e:
    logger.error(e)
    sys.stdin.readline()

app = default_app()
