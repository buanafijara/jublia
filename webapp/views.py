from flask import Blueprint, render_template, request
from .models import Event, Email, Task
from . import db, scheduler, send_email
from datetime import datetime
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    text = '''go to /all to see all events''' 
    return render_template('home.html', html_page_text=text)

@views.route('/save_emails', methods=['GET', 'POST'])
def save_emails():
    if request.method == 'POST':
        event_id = request.form['event_id']
        email_subject = request.form['email_subject']
        email_content = request.form['email_content']
        timestamp = datetime.strptime(request.form['timestamp'], '%Y-%m-%d %H:%M')
        event0 = Task(event_id=event_id, 
                    email_subject=email_subject,
                    email_content=email_content,
                    timestamp=timestamp
                    )
        db.session.add(event0)
        db.session.commit()

        emails_q = Email.query.join(Event.participants).filter(Event.id==event_id).all()
        emails = [email.email for email in emails_q]

        scheduler.add_job(send_email, 'date', run_date=timestamp, args=[emails, email_subject, email_content, timestamp])
    return render_template('save_emails.html')

@views.route('/event_list', methods=['GET', 'POST'])
def event_list():
    if request.method == 'POST':
        event = Event(name = request.form['name'])
        db.session.add(event)
        db.session.commit()       

    events = Event.query.all()

    return render_template('events.html', events=events)

@views.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        email = Email(email = request.form['email'])
        event_id = request.form['event_id']
        event = Event.query.get(event_id)
        email.followed_events.append(event)
        db.session.add(email)
        db.session.commit()       

    emails = Email.query.all()

    return render_template('user.html', emails=emails)

@views.route('/task', methods=['GET', 'POST'])
def task():
    tasks = Task.query.all()
    for task in tasks:
        event = Event.query.get(task.event_id)
        emails = Email.query.join(Event.participants).filter(Event.id==event.id).all()
        task.participants = [email.email for email in emails]
    with open('log.json') as f:
        logs = json.load(f)
    context = {
        'tasks': tasks,
        'logs': logs
    }
    return render_template('task.html', context=context)