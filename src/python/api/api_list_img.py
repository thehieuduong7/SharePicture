from base64 import b64encode  # or urlsafe_b64decode
import base64
import flask
from urllib.error import URLError, HTTPError
import os
import urllib
from flask import request, url_for, session, jsonify
from flask_login.utils import login_required
from flask_login import current_user, login_user
from __init__ import app
import json

from models import PictureModel
from src.python.service.Service import AuthService, PictureService, ShareService

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


picSer = PictureService()
shareSer = ShareService()
auSer = AuthService()


def savePic(image_64_encode, user_id, file_name):
    try:
        os.makedirs("static/uploads/"+str(user_id))
    except FileExistsError:
        print('exist')

    file_name = 'static/uploads/'+file_name  # "userid/pic.png"

    # ---------------------------------------------------------------

    # image_64_encode là "data:img/png;base64 ....."
    resource = urllib.request.urlopen(image_64_encode)

    with open(file_name, "wb") as output:

        read = resource.read()
        # encode   convert bytes  to bytes     b'0x41/0x32'
        enRead = read

        output.write(enRead)
        output.close()


@app.route("/mypicture/upload_img", methods=["POST"])
@login_required
def upload_img():
    user_id = current_user.id
    data = request.get_json(force=True)
    image_64_encode = data['readfile']
    file_name = data['name']
    pic = picSer.insert(user_id, file_name)
    if(pic):
        # pic.pic = "userid/pic.png"
        savePic(image_64_encode, user_id, pic.pic)
        res = True
    else:
        res = False
    res = {
        'success': res
    }
    return json.dumps(res)


@login_required
@app.route("/mypicture/getPictures", methods=["GET"])
def getPictures():
    user_id = current_user.id
    pics = picSer.getByUserID(user_id)
    pictures = [{'picture_id': i.id}.copy() for i in pics]
    map = {
        "userlogin_id": current_user.id,
        "picture_ids": pictures
    }
    return json.dumps(map)


@login_required
@app.route("/mypicture/searchPicture/<int:picture_id>", methods=["GET"])
def searchPicture(picture_id):
    user_id = current_user.id
    pic = picSer.searchByPicID(user_id, picture_id)
    if(pic == None):
        return ""

    url_img = 'static/uploads/'+pic.pic  # url trong folder

    # ----------------
    try:
        with open(url_img, "rb") as output:
            decode = output.read()

        # convert byte to data urls
        b64_mystring = b64encode(decode).decode("utf-8")
        url_img = "data:image/png;base64,"+b64_mystring
    except HTTPError as e:
        print('Error code: ', e.code)
    except FileNotFoundError as e:
        print('Reason: ', e)

    map = {
        "picture_id": pic.id,
        "create_at": str(pic.create_at),
        "pic": url_img,
        "userlogin_id": pic.userlogin_id,
        "fullname": pic.userlogin.fullname,
        "username": pic.userlogin.username
    }
    return json.dumps(map, default=str)


@login_required
@app.route("/sharepicture/getShare", methods=["GET"])
def getPictureShared():
    user_id = current_user.id
    shares = shareSer.getByUserID(user_id)
    pictures = [{'picture_id': i.picture_id, }.copy() for i in shares]
    map = {
        "userlogin_id": current_user.id,
        "picture_ids": pictures
    }
    return json.dumps(map)


@login_required
@app.route("/sharepicture/shareFor/<int:picture_id>", methods=["GET"])
def listShareFor(picture_id):
    user_id = current_user.id
    if not picSer.is_Permission(user_id, picture_id):
        return ""
    shares = shareSer.searchByPicID(picture_id)
    userAvail = shareSer.searchAvailableUser(picture_id)
    list_share = [{'userlogin_id': sh.userlogin_id, }.copy()
                  for sh in shares]
    list_avail = [{'userlogin_id': u.id}.copy()
                  for u in userAvail]

    map = {
        "userlogin_id": user_id,
        "picture_id": picture_id,
        "share_user_id": list_share,
        "available_user_id": list_avail
    }
    return json.dumps(map)

# @login_required


@app.route("/sharepicture/shareTo", methods=["POST", "DELETE"])
def shareTo():
    user_id = current_user.id
    data = request.get_json(force=True)
    picture_id = data['picture_id']
    username = data['username']
    user = auSer.getByUsername(username)
    if(not user):
        res = False
        mess = "User not found"

    elif(not picSer.is_Permission(user_id, picture_id)):
        res = False
        mess = "Bạn không có quyền chia sẽ"
    else:
        if(request.method == "POST"):
            res = not not shareSer.insert(picture_id, user.id)
            mess = "Sharing success" if res else "Shared"
        else:
            res = not not shareSer.remove(picture_id, user.id)
            mess = "Delete success" if res else "Server error"

    map = {
        "success": res,
        "message": mess
    }
    return json.dumps(map)
