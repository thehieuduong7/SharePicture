import jwt

token = jwt.encode({'thehieu': '1'}, 'my-secret', algorithm='HS256')