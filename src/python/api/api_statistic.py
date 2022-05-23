from __init__ import app, my_login
import json
from flask_login import login_user
from models import UserLoginModel
from src.python.service.Service import AuthService, StatisticService

static = StatisticService()


@app.route('/static/shared')
def statisticShare():
    list = static.getStatisticShared()
    res = []
    for i in list:
        u = UserLoginModel.query.get(i[0])
        res.append((i[0], u.fullname, i[1]))
    return json.dumps({"statistic": res})
