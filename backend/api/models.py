from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, default=0)
    task_id = db.Column(db.Integer, nullable=True)

class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(255), nullable=False)
    passed = db.Column(db.Boolean, default=False)
    file_id = db.Column(db.String(255), nullable=True)

class Votes(db.Model):
    __tablename__ = "votes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    task_id = db.Column(db.Integer, nullable=False)
    vote_value = db.Column(db.Integer, default=0)
