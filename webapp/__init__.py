from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import json
from datetime import datetime

db = SQLAlchemy()
DB_NAME = "database.db"
scheduler = BackgroundScheduler(timezone='Asia/Singapore')
scheduler.start()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .views import views

    app.register_blueprint(views, url_prefix='/')

    from .models import Email, Event, Task
    create_database(app)

    return app

def create_database(app):
    if not path.exists('webapp/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')

def send_email(emails, email_subject, email_content, timestamp):

    # send emails to the given address with the given details via SMTP service
    
    # track the execution by logging
    printLog(f'email sent to {emails} at {timestamp}')

def printLog(content):
    now = datetime.now()
    filename = 'task.json'
    output = {
        'message': content
    }
    
    with open(filename) as f:
        listObj = json.load(f)
        
    listObj.append(output)

    with open(filename, 'w') as f:
        json.dump(listObj, f, indent=4, separators=(',',': '))
    # msg = f'{now} --- {content}'
    # with open('/home/project/fms/print.txt', 'r') as original: 
    #     data = original.read()
    # with open('/home/project/fms/print.txt', 'w') as modified: 
    #     modified.write(msg + "\n" + data)
