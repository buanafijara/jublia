#!/usr/bin/env python
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from flask import Flask,json, render_template, request, jsonify, make_response
import json
import os
#create instance of Flask app
app = Flask(__name__)
scheduler = BackgroundScheduler(timezone='Asia/Singapore')
scheduler.start()

def send_email(timestamp):
    print(f'email sent at {timestamp}')

@app.route("/") 
def hello():
    #it is a good idea to 
    #include information on how 
    #to use your API on the home 
    #route
    text = '''go to /all to see all events''' 
    return render_template('index.html', html_page_text=text)
  
@app.route("/save_emails", methods=['POST']) 
def save_emails(): 
    if request.method == 'POST':
        params = {
            'event_id' : request.form['event_id'],
            'email_subject' : request.form['email_subject'],
            'email_content' : request.form['email_content'],
            'timestamp' : request.form['timestamp']
        }
        scheduler.add_job(send_email, 'date', run_date=datetime.strptime(params['timestamp'], '%Y-%m-%d %H:%M'), args=[params['timestamp']])
        response = make_response(
            jsonify(params),
            401,
        )
        response.headers["Content-Type"] = "application/json"
        return response

if __name__ == "__main__":
    app.run(debug=True)
