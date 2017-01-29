from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from gevent.wsgi import WSGIServer
from settings import *
import requests
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(24).encode("hex")
s = requests.Session()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_cards")
def get_cards():
    data = json.loads(open("sample.json").read())
    return json.dumps(data)

def auth():
    auth_payload = {
            "grant_type": "password",
            "client_id": client_id,
            "client_secret": client_secret,
            "username": username,
            "password": password
            }

    r = s.post("https://api.gfycat.com/v1/oauth/token", data=json.dumps(auth_payload))
    s.headers.update({"Authorization": str("Bearer " + r.json()["access_token"])})
    data = json.loads(r.text)
    at = data["access_token"]
    print "lovely: " + at
    return at

def auth_session():
    auth_payload = {
            "grant_type": "password",
            "client_id": client_id,
            "client_secret": client_secret,
            "username": username,
            "password": password
            }

    r = s.post("https://api.gfycat.com/v1/oauth/token", data=json.dumps(auth_payload))
    s.headers.update({"Authorization": str("Bearer " + r.json()["access_token"])})
    data = json.loads(r.text)
    at = data["access_token"]
    print "lovely: " + at
    return s

def returnerror(message):
    return {"error": str(message)}

def to_json(data):
    returnobj = {'results': len(data), 'data': []}
    for gfy in data:
        try:
            returnobj['data'].append({
                "id": gfy["gfyId"], "likes": gfy["likes"], "dislikes": gfy["dislikes"],
                "url": gfy["gifUrl"], "tags":gfy["tags"], "userName": gfy["userName"], 
                "title": gfy["title"], "description": gfy["description"], "createDate": gfy["createDate"]
            })
        except Exception, e:
            returnobj['data'].append(returnerror(str(e)))
    return jsonify(returnobj)

def update_user_json(tags):
    with open('user.json', 'r') as f:
        json_data = json.load(f)
    for tag in tags:
        if tag in json_data['tags']:
            json_data['tags'][tag] += 1
        else:
            json_data['tags'][tag] = 1

    with open('user.json', 'w') as f:
        f.write(json.dumps(json_data))  

# http://localhost:8000/api/get_trending_tag?tag=gaming?count=5
# @app.route('/api/get_trending_tag', methods=['GET'])
def get_trending_tag(tag, count):
    # **********************************************
    # Always get the access token because - hackathon
    at = auth()
    # **********************************************
    # tag = request.args.get("tag")
    # count = request.args.get("count")
    r = requests.get('https://api.gfycat.com/v1/gfycats/trending?access_token=' + at + '&count=' + str(count) + '&tagName=' + tag)
    data = json.loads(r.text)
    return  data

# http://localhost:8000/api/get_trending_tag_testing?tag=gaming&count=5
@app.route('/api/get_trending_tag', methods=['GET'])
def get_trending_tag_testing():
    # **********************************************
    # Always get the access token because - hackathon
    at = auth()
    # **********************************************
    tag = request.args.get("tag")
    count = request.args.get("count")
    r = requests.get('https://api.gfycat.com/v1/gfycats/trending?access_token=' + at + '&count=' + str(count) + '&tagName=' + tag)
    data = json.loads(r.text)
    return  to_json(data["gfycats"])

# http://localhost:8000/api/get_trending?count=5
@app.route('/api/get_trending', methods=['GET'])
def get_trending():
    # **********************************************
    # Always get the access token because - hackathon
    at = auth()
    # **********************************************

    count = request.args.get("count")
    r = requests.get('https://api.gfycat.com/v1/gfycats/trending?access_token=' + at + '&count=' + count)
    data = json.loads(r.text)
    return to_json(data["gfycats"])
    
    

@app.route('/api/get_user_info', methods=['GET'])
def get_user_info():
    # **********************************************
    # Always get the access token because - hackathon
    # s = auth_session()
    # **********************************************
    # returnobj = {'results': len(data), 'data': []}
    # r = s.get('https://api.gfycat.com/v1/me')
    tags = request.args.get("tags")
    if tags:
        tags_arr = tags.split(',')
        update_user_json(tags_arr)

    with open('user.json') as json_data:
        data = json.load(json_data)
    return jsonify(data)

@app.route('/api/get_recommended', methods=['GET'])
def get_recommended():
    with open('user.json') as json_data:
        data = json.load(json_data)
    max_value = 0
    max_value_tag = ''

    count = request.args.get("count")
    for tag in data['tags']:
        if data['tags'][tag] > max_value:

            max_value = data['tags'][tag]
            max_value_tag = tag
            print max_value, max_value_tag
    data = get_trending_tag(max_value_tag, count)
    return to_json(data['gfycats'])


# If i have the fking time
# @app.route('/api/get_search', methods=['GET'])
# def get_search():
#         # **********************************************
#     # Always get the access token because - hackathon
#     at = auth()
#     # **********************************************
#     r = requests.get('https://api.gfycat.com/v1test/gfycats/trending?count=100')
#     return gfycats_tag[0]


http_server = WSGIServer(("", PORT), app)
http_server.serve_forever()
