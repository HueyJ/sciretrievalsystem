from datetime import datetime
from webapp import db


class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    search_terms = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_ip = db.Column(db.Integer)

    def __repr__(self):
        return '<SearchHistory {}>'.format(self.body)
