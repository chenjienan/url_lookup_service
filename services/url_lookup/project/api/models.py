from sqlalchemy.sql import func
from project import db

class Url(db.Model):
    __tablename__ = 'url_list'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, url):
        self.url = url