from . import db

transaction_event = db.Table('transaction_event',
    db.Column('transaction_id', db.Integer, db.ForeignKey('transaction.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
    )

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    followed_events = db.relationship('Event', secondary=transaction_event, backref=db.backref('participants', lazy='dynamic'))

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