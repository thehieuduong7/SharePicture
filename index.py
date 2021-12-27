from flask import render_template,url_for
from __init__ import app
from api.api_login import *
from api.api_list_img import *

@app.route("/",methods=["Get"])
def home():
    return redirect(url_for("list_img"))
 
@app.route("/auth",methods=["Get"])
def auth():
    return render_template("decorators/login.html")

@app.route("/list_img",methods=["Get"])
def list_img():
    return render_template("views/list_image.html")

if(__name__=="__main__"):
    with app.app_context():
        app.run(debug=1)

