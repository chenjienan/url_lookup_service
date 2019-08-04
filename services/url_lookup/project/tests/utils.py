from project import db
from project.api.models import Url


def add_url(url):
    cur_url = Url(url=url)
    db.session.add(cur_url)
    db.session.commit()
    return cur_url
