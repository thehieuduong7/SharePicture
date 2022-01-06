from flask import render_template, request, redirect, session, jsonify
from flask_login.utils import login_required, logout_user
from flask_login import current_user, login_user
from __init__ import app,my_login
import json
from flask_login import login_user
from src.python.service.Service import AuthService

auSer = AuthService()
@my_login.user_loader
def load_user(user_id):
    return auSer.getByID(user_id) 

@app.route("/login",methods=["POST"])
def login():
    data = request.get_json(force=True)
    usr = data["username"]
    pwd = data["password"]
    u = auSer.login(usr,pwd)
    if u==None:
        res=False
    else:
        res=login_user(user=u)
    res = {
        'success': res,
    }
    return json.dumps(res)

@app.route("/register",methods=["POST"])
def register():
    data = request.get_json(force=True)
    usr = data["username"]
    pwd = data["password"]
    name = data['fullname']
    key_n=data['key_n']
    key_e=data['key_e']
    u =auSer.register(usr,pwd,name)
    if u==None:
        res=False
    else:
        res=login_user(user=u)
    res = {
        'success': res,
    }

    return json.dumps(res)

@login_required
@app.route("/logout",methods=["Get"])
def logout():
    logout_user()
    res=True
    res = {
        'success': res
    }
    return json.dumps(res)

@login_required
@app.route("/userlogin/all",methods=["Get"])
def userloginAll():
    list = auSer.getAll()
    userlogins=[]
    for u in list:
        map ={
            'userlogin_id':u.id,
            'fullname':u.fullname,
            'username':u.username
        }
        userlogins.append(map.copy())
    map = {
        "userlogins":userlogins
    }
    return json.dumps(map)


@login_required
@app.route("/userlogin/search/<int:userlogin_id>",methods=["Get"])
def userlogigsearch(userlogin_id):
    u = auSer.getByID(userlogin_id)
    map ={
            'userlogin_id':u.id,
            'fullname':u.fullname,
            'username':u.username
        }
    return json.dumps(map)
