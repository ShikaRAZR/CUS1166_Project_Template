
# import flask_wtf
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField, DateTimeField, IntegerField, FloatField
from wtforms.validators import ValidationError, DataRequired, Length



class TaskForm(FlaskForm):
    task_desc = StringField('task_desc', validators=[DataRequired()])
    task_status_completed = SelectField('Status', choices=[('todo','Todo'),('doing','Doing'),('done','Done')])
    submit = SubmitField('submit')

class AppointmentForm(FlaskForm):
    appointment_title = StringField('Appointment Title', validators=[DataRequired()])
    appointment_start_date = DateTimeField('Start Time', validators=[DataRequired()])
    appointment_duration = StringField('Duration', validators=[DataRequired()])
    appointment_location = StringField('Customer Address', validators=[DataRequired()])
    customer_name = StringField('Customer Name', validators=[DataRequired()])
    customer_notes = StringField('Customer Notes', validators=[DataRequired()])
    submit = SubmitField('submit')
