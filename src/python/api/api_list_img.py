from flask import render_template, request, redirect, session, jsonify
from __init__ import app
import json

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

import base64
import urllib
@app.route("/upload_img",methods=["POST"])
def upload_img():
    data = request.get_json(force=True)
    
    file_name= data['name']
    image_64_encode= data['readfile']
    response = urllib.request.urlopen(image_64_encode)
    with open(file_name, 'wb') as f:
        f.write(response.file.read())
        return 'done'
    return 'error'
