from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from config import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    # return 0

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String, unique=True, nullable=False)
    senha = db.Column(db.String, nullable=False)
    events = db.relationship('Event', backref='owner', lazy=True)


event_participants = db.Table('event_participants',
                              db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
                              db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
                              )


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relacionamento com os participantes (muitos-para-muitos)
    participants = db.relationship('User', secondary=event_participants, lazy='subquery',
                                   backref=db.backref('participated_events', lazy=True))