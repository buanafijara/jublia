from flask import Blueprint, render_template, request, jsonify
from .models import Event, Transaction, Task
from . import db, scheduler, send_email
from datetime import datetime
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/save_emails', methods=['GET', 'POST'])
def save_emails():
    """save and schedule emails that needed to be sent"""

    if request.method == 'POST':
        event_id = request.form['event_id']
        email_subject = request.form['email_subject']
        email_content = request.form['email_content']
        timestamp = datetime.strptime(request.form['timestamp'], 
                                    '%Y-%m-%d %H:%M')

        # add instance to database
        event0 = Task(event_id=event_id, 
                    email_subject=email_subject,
                    email_content=email_content,
                    timestamp=timestamp
                    )
        db.session.add(event0)
        db.session.commit()

        # get registered emails for the event
        emails_q = Transaction.query.join(Event.participants)\
                    .filter(Event.id==event_id).all()
        emails = [email.email for email in emails_q]

        # schedule a job to send the emails
        scheduler.add_job(send_email, 
                        'date', 
                        run_date=timestamp, 
                        args=[emails, email_subject, email_content, timestamp])

        message = 'Task have been scheduled and will be executed accordingly.'
        result = {
            'status': 200,
            'message': message
        }
        return jsonify(result)
        
    return render_template('save_emails.html')

@views.route('/event_list', methods=['GET', 'POST'])
def event_list():
    """GUI to help monitor the content of the Event table"""

    if request.method == 'POST':
        event = Event(name = request.form['name'])
        db.session.add(event)
        db.session.commit()       

    events = Event.query.all()

    return render_template('events.html', events=events)

@views.route('/transaction', methods=['GET', 'POST'])
def transaction():
    """GUI to help monitor the content of he Transaction table"""

    if request.method == 'POST':
        email = Transaction(email = request.form['email'])
        event_id = request.form['event_id']
        event = Event.query.get(event_id)
        email.followed_events.append(event)
        db.session.add(email)
        db.session.commit()       

    emails = Transaction.query.all()

    return render_template('transaction.html', emails=emails)

@views.route('/task', methods=['GET', 'POST'])
def task():
    """GUI to monitor the content of Task table and whether the emails 
    have been sent"""

    tasks = Task.query.all()
    for task in tasks:
        event = Event.query.get(task.event_id)
        emails = Transaction.query.join(Event.participants)\
                .filter(Event.id==event.id).all()
        task.participants = [email.email for email in emails]
    with open('log.json') as f:
        logs = json.load(f)
    context = {
        'tasks': tasks,
        'logs': logs
    }
    return render_template('task.html', context=context)