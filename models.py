
from flask_login import UserMixin
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    date_registered = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_admin = db.Column(db.Boolean, default=False)
    predictions = db.relationship('Prediction', back_populates='user', lazy=True)

    def __repr__(self):
        return f'User("{self.name}", "{self.email}")'

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(20), default='pending')  # pending, responded, closed

    def __repr__(self):
        return f'Contact("{self.name}", "{self.email}", "{self.date}")'

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    population = db.Column(db.Integer)
    temperature_increase = db.Column(db.Float)
    urban_density = db.Column(db.String(20))
    infrastructure = db.Column(db.String(20))
    risk_level = db.Column(db.String(20))
    risk_score = db.Column(db.Float)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user = db.relationship('User', back_populates='predictions')

    def __repr__(self):
        return f'Prediction("{self.city}", "{self.risk_level}", "{self.date}")'
