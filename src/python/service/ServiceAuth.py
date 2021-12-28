from models import *

class AuthService():
    def login(self,username,password):
        username = username.strip()
        password = password.strip()

        u = UserLoginModel.query.filter(UserLoginModel.username==username,
            UserLoginModel.password==password).first()
        return u
    


    
