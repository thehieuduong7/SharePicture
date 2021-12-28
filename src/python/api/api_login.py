from flask import render_template, request, redirect, session, jsonify
from flask_login.utils import logout_user
from __init__ import app,my_login
import json
from flask_login import login_user
from models import UserLoginModel
from src.python.service.ServiceAuth import AuthService

@my_login.user_loader
#Bỏ cả đối tượng vào biến current_user
def user_load(user_id):
    return UserLoginModel.query.get(user_id)

@app.route("/login",methods=["POST"])
def login():
    data = request.get_json(force=True)
    usr = data["username"]
    pwd = data["password"]
    au = AuthService()
    u = au.login(usr,pwd)
    print(u)
    if u==None:
        res=False
    else:
        login_user(u)
        res=True
    res = {
        'success': res
    }
    return json.dumps(res)

@app.route("/register",methods=["POST"])
def register():
    data = request.get_json(force=True)
    usr = data["username"]
    pwd = data["password"]
    return json.dumps(data)


@app.route("/logout",methods=["Get"])
def logout():
    logout_user()
    res=True
    res = {
        'success': res
    }
    return json.dumps(res)