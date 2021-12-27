from flask import render_template, request, redirect, session, jsonify
from __init__ import app
import json


@app.route("/login",methods=["POST"])
def login():
    data = request.get_json(force=True)
    usr = data["username"]
    pwd = data["password"]
    return json.dumps(data)

@app.route("/register",methods=["POST"])
def register():
    data = request.get_json(force=True)
    usr = data["username"]
    pwd = data["password"]
    return json.dumps(data)