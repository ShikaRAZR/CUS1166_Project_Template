
# import flask_wtf
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length




class TaskForm(FlaskForm):
    task_desc = StringField('task_desc', validators=[DataRequired()])
    task_status_completed = SelectField('Status', choices=[('todo','Todo'),('doing','Doing'),('done','Done')])
    submit = SubmitField('submit')
