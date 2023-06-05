from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), unique=True)
    
    def get_id(self):
        return str(self.user_id)

class Movie(db.Model):
    movie_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date_added = db.Column(db.Date, default=db.func.current_date())
    extension = db.Column(db.String(10), nullable=False)
    url = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship('User', backref='movies')

class MovieWithDetection(db.Model):
    movie_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date_added = db.Column(db.Date, default=db.func.current_date())
    extension = db.Column(db.String(10), nullable=False)
    url = db.Column(db.String(250))
    
    annotations = db.Column(db.String(10000))
    source_movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'))
    source_movie = db.relationship('Movie', backref='detections')
