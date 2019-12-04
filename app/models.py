
#from flask import url_for
from app import db
from datetime import datetime




class Task(db.Model):

    task_id = db.Column(db.Integer, primary_key=True)
    task_desc = db.Column(db.String(128), index=True)
    task_status = db.Column(db.String(128))


class Appointment(db.Model):
    appointment_id = db.Column(db.Integer, primary_key=True)
    appointment_title = db.Column(db.String)
    appointment_start_date = db.Column(db.DateTime)
    appointment_duration = db.Column(db.String)
    appointment_location = db.Column(db.String)
    customer_name = db.Column(db.String)
    customer_notes = db.Column(db.String)
