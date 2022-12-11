from . import db

email_event = db.Table('email_event',
    db.Column('email_id', db.Integer, db.ForeignKey('email.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
    )

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    followed_events = db.relationship('Event', secondary=email_event, backref=db.backref('participants', lazy='dynamic'))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    email_subject = db.Column(db.String(150))
    email_content = db.Column(db.String(10000))
    timestamp = db.Column(db.DateTime(10000))

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    task = db.relationship('Task', backref='event')