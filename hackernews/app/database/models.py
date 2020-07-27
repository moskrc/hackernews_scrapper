import datetime

from app.database import db


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    id_hn = db.Column(db.Integer, index=True)
    title = db.Column(db.String(255))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_hn = db.Column(db.DateTime)
    url = db.Column(db.String(255))

    def __repr__(self):
        return '<Post \'%s\'>' % self.title
