from flask import render_template, request, redirect, session, jsonify
from flask_login.utils import login_required
from flask_login import current_user, login_user
from sqlalchemy.sql.functions import user
from __init__ import app
import json

from models import PictureModel
from src.python.service.Service import AuthService, PictureService, ShareService

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

import base64
import urllib

picSer = PictureService()
shareSer = ShareService()
auSer = AuthService()
@app.route("/mypicture/upload_img",methods=["POST"])
@login_required
def upload_img():
    user_id = current_user.id
    data = request.get_json(force=True)
    image_64_encode= data['readfile']
    file_name= data['name']
    response = urllib.request.urlopen(image_64_encode)
    with open(file_name, 'wb') as f:    #check open duoc ko
        res = picSer.insert(user_id,image_64_encode)
    res = {
        'success': res
    }
    return json.dumps(res)

@login_required
@app.route("/mypicture/getPictures",methods=["GET"])
def getPictures():
    user_id = current_user.id
    pics = picSer.getByUserID(user_id)    
    pictures = []
    if pics:
        for i in pics:
            map={
                'picture_id':i.id,
            }
            pictures.append(map.copy())
    map={
        "userlogin_id":current_user.id,
        "username":current_user.username,
        "fullname":current_user.fullname,
        "picture_ids":pictures
    }
    return json.dumps(map)


@login_required
@app.route("/mypicture/searchPicture/<int:picture_id>",methods=["GET"])
def searchPicture(picture_id):
    user_id = current_user.id
    pic = picSer.searchByPicID(user_id,picture_id)
    if(pic==None): return ""
    map={
        "picture_id": pic.id,
        "create_at": str(pic.create_at),
        "pic": pic.pic,
        "userlogin_id":pic.userlogin_id,
        "fullname": pic.userlogin.fullname,
        "username": pic.userlogin.username
    }
    return json.dumps(map,default=str)


#list cac picture duoc shaare cho usser
@login_required
@app.route("/sharepicture/getShare",methods=["GET"])
def getPictureShared():
    user_id = current_user.id
    shares = shareSer.getByUserID(user_id)    
    pictures = []
    if shares:
        for i in shares:
            map={
                'picture_id':i.picture_id,
            }
            pictures.append(map.copy())
    map={
        "userlogin_id":current_user.id,
        "username":current_user.username,
        "fullname":current_user.fullname,
        "picture_ids":pictures
    }
    return json.dumps(map)


@login_required
@app.route("/sharepicture/shareFor/<int:picture_id>/<int:is_full>",methods=["GET"])
def listtShareFor(picture_id,is_full):
    user_id = current_user.id
    if not not picSer.is_Permission(user_id,picture_id): return ""
    shares = shareSer.getByUserID(picture_id)    
    list_user = []
    if( shares):
        for i in shares:
            map={
                'userlogin_id':i.userlogin_id,
            }
            list_user.append(map.copy())
    map={
        "picture_id":picture_id,
        "share_user_id":list_user
    }
    return json.dumps(map)

#@login_required
@app.route("/sharepicture/shareTo",methods=["POST","DELETE"])
def shareTo():
    user_id = 1#current_user.id
    data = request.get_json(force=True)
    picture_id= data['picture_id']
    userlogin_id = data['userlogin_id']
    
    if(not picSer.is_Permission(user_id,picture_id)):
        res=False
    else:  
        if(request.method=="POST"):
            res = not not shareSer.insert(picture_id,userlogin_id)
        else:
            res = not not shareSer.remove(picture_id,userlogin_id)
    map={
        "success":res
    }
    return json.dumps(map)




