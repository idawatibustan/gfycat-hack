from flask import Flask, render_template, request, redirect, url_for, session
from gevent.wsgi import WSGIServer
from settings import *
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(24).encode("hex")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_cards")
def get_cards():
    data = json.loads(open("sample.json").read())
    return json.dumps(data)

http_server = WSGIServer(("", PORT), app)
http_server.serve_forever()
