from __init__ import app, my_login
import json
from flask_login import login_user
from models import UserLoginModel


@app.route('/static')
def statisticApi():
    all = UserLoginModel.query.all()
    res = []
    for u in all:
        count_pictures = (len(u.pictures))
        count_shared_to_me = (len(u.shares))
        count_share_to_everybody = 0
        for pic in u.pictures:
            count_share_to_everybody += len(pic.shares)
        print(count_pictures, count_shared_to_me, count_share_to_everybody)
        res.append({"id": u.id, "fullname": u.fullname, 'count_pictures': count_pictures,
                    "count_shared_to_me": count_shared_to_me, "count_share_to_everybody": count_share_to_everybody
                    })
    return json.dumps({"statistic": res})
