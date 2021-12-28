from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView, Admin

from __init__ import db, app
from models import *

admin = Admin(app=app, name = "UTE SHOP", template_mode = 'bootstrap4')


class userModelView(ModelView):
    can_export = True
    can_view_details = True


    column_labels = dict(fullname = "full",
                        username = "username",password="pass")

    can_set_page_size = True

class imgModelView(ModelView):
    can_export = True
    column_labels = dict(create_at="create",pic = "pic",
                        userlogin_id = "username_id")    




class shareModelView(ModelView):
    can_export = True
    can_view_details = True  
    column_labels = dict(picture_id = "pic",
                        userlogin_id = "username")  
    
admin.add_view(userModelView(UserLoginModel, db.session, name = "user"))
admin.add_view(imgModelView(PictureModel, db.session, name = "pictur"))
admin.add_view(shareModelView(SharePicture, db.session, name = "share"))
