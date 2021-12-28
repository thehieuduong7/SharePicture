from flask import render_template,url_for,redirect
from __init__ import app
from src.python.api.api_login import *
from src.python.api.api_list_img import *
from admin import *
from flask_login import current_user, login_user

@app.route("/",methods=["Get"])
def home():
    if(not current_user.is_authenticated):
        return redirect(url_for("auth"))
    return redirect(url_for("list_img"))
 
@app.route("/auth",methods=["Get"])
def auth():
    return render_template("decorators/login.html")

@app.route("/list_img",methods=["Get"])
def list_img():
    if(not current_user.is_authenticated):
        return redirect(url_for("auth"))
    return render_template("views/list_image.html")

if(__name__=="__main__"):
    with app.app_context():
        app.run(debug=1)


