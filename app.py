from flask import Flask, request, redirect, url_for, session
from gevent.wsgi import WSGIServer
from settings import *
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(24).encode("hex")

@app.route("/")
def home():
    return json.dumps({"Hello": "World"})

http_server = WSGIServer(("", PORT), app)
http_server.serve_forever()
