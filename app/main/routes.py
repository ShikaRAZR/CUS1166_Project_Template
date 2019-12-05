from flask import render_template,  redirect, url_for
from app.main import bp
from app import db
from app.main.forms import TaskForm, AppointmentForm, SearchForm
from app.models import Task, Appointment
from datetime import datetime
from datetime import datetime as dt



# Main route of the applicaitons.
@bp.route('/', methods=['GET','POST'])
def index():
    return render_template("main/index.html")


#
#  Route for viewing and adding new tasks.
@bp.route('/todolist', methods=['GET','POST'])
def todolist():
    form = TaskForm()

    if form.validate_on_submit():
        # Get the data from the form, and add it to the database.
        new_task = Task()
        new_task.task_desc =  form.task_desc.data
        new_task.task_status = form.task_status_completed.data

        db.session.add(new_task)
        db.session.commit()

        # Redirect to this handler - but without form submitted - gets a clear form.
        return redirect(url_for('main.todolist'))

    todo_list = db.session.query(Task).all()

    return render_template("main/todolist.html",todo_list = todo_list,form= form)


#
# Route for removing a task
@bp.route('/todolist/remove/<int:task_id>', methods=['GET','POST'])
def remove_task(task_id):

    # Query database, remove items
    Task.query.filter(Task.task_id == task_id).delete()
    db.session.commit()

    return redirect(url_for('main.todolist'))


#
# Route for editing a task

@bp.route('/todolist/edit/<int:task_id>', methods=['GET','POST'])
def edit_task(task_id):
    form = TaskForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        # Get the data from the form, and add it to the database.

        current_task = Task.query.filter_by(task_id=task_id).first_or_404()
        current_task.task_desc =  form.task_desc.data
        current_task.task_status = form.task_status_completed.data

        db.session.add(current_task)
        db.session.commit()
        # After editing, redirect to the view page.
        return redirect(url_for('main.todolist'))

    # get task for the database.
    current_task = Task.query.filter_by(task_id=task_id).first_or_404()

    # update the form model in order to populate the html form.
    form.task_desc.data =     current_task.task_desc
    form.task_status_completed.data = current_task.task_status

    return render_template("main/todolist_edit_view.html",form=form, task_id = task_id)


#
#  Route for viewing and adding new tasks.
@bp.route('/appointmentlist/<int:sortby>/', methods=['GET','POST'])
def appointmentlist(sortby):
    form = AppointmentForm()

    if form.validate_on_submit():
        # Get the data from the form, and add it to the database.
        new_appointment = Appointment(appointment_title=form.appointment_title.data,
                                      appointment_start_date=form.appointment_start_date.data,
                                      appointment_duration = form.appointment_duration.data,
                                      appointment_location = form.appointment_location.data,
                                      customer_name = form.customer_name.data,
                                      customer_notes = form.customer_notes.data)

        db.session.add(new_appointment)
        db.session.commit()
        # Redirect to this handler - but without form submitted - gets a clear form.
        return redirect(url_for('main.appointmentlist', sortby=sortby))

    if sortby==0:
        appointment_list = Appointment.query.order_by(Appointment.appointment_title)
    elif sortby==1:
        appointment_list = Appointment.query.order_by(Appointment.appointment_start_date)
    elif sortby==2:
        appointment_list = Appointment.query.order_by(Appointment.appointment_duration)
    elif sortby==3:
        appointment_list = Appointment.query.order_by(Appointment.appointment_location)
    elif sortby==4:
        appointment_list = Appointment.query.order_by(Appointment.customer_name)
    elif sortby==5:
        appointment_list = Appointment.query.order_by(Appointment.customer_notes)
    else:
        appointment_list = db.session.query(Appointment).all()
    return render_template("main/appointmentlist.html",appointment_list = appointment_list,form= form, sortby=sortby)



@bp.route('/appointmentlist/remove/<int:appointment_id>', methods=['GET','POST'])
def remove_appointment(appointment_id):
    # Query database, remove items
    print(appointment_id)
    Appointment.query.filter(Appointment.appointment_id == appointment_id).delete()
    db.session.commit()
    return redirect(url_for('main.appointmentlist', sortby=0))

@bp.route('/appointment/<int:appointment_id>', methods=['GET','POST'])
def appointment(appointment_id):
    form = AppointmentForm()
    if form.validate_on_submit():
        # Get the data from the form, and add it to the database.
        modified_appointment = Appointment(appointment_title=form.appointment_title.data,
                                      appointment_start_date=form.appointment_start_date.data,
                                      appointment_duration = form.appointment_duration.data,
                                      appointment_location = form.appointment_location.data,
                                      customer_name = form.customer_name.data,
                                      customer_notes = form.customer_notes.data)
        Appointment.query.filter(Appointment.appointment_id == appointment_id).delete()
        db.session.commit()
        db.session.add(modified_appointment)
        db.session.commit()

    appointment=Appointment.query.filter(Appointment.appointment_id == appointment_id).one()
    return render_template("main/appointment.html",appointment = appointment,form= form, appointment_id=appointment_id)

@bp.route('/appointmentsearch/<int:filterby>', methods=['GET','POST'])
def search_appointment(filterby):
    def sameDay(now,specificAppointmentTime):
        #print(specificAppointmentTime.year, now.year, specificAppointmentTime.month,now.month, specificAppointmentTime.day,now.day)
        return specificAppointmentTime.year==now.year and specificAppointmentTime.month==now.month and specificAppointmentTime.day==now.day
    def sameWeek(now,specificAppointmentTime):
        #print(now.isocalendar()[1], specificAppointmentTime.isocalendar()[1], now.year, specificAppointmentTime.year)
        return now.isocalendar()[1]==specificAppointmentTime.isocalendar()[1] and now.year==specificAppointmentTime.year

    appointment_list = Appointment.query.all()
    now = datetime.now()


    if filterby==0:#No Filter
        print('No Filter')
    elif filterby==1:#Filter for today
        for appointment in reversed(appointment_list):#if not reversed, array will skip certian items when removed
            if not sameDay(now, appointment.appointment_start_date):
                appointment_list.remove(appointment)
    elif filterby==2:#Filter for this week
        for appointment in reversed(appointment_list):#if not reversed, array will skip certian items when removed
            if not sameWeek(now, appointment.appointment_start_date):
                appointment_list.remove(appointment)
    elif filterby==3:#Filter Overdue (Everything before current datetime)
        for appointment in reversed(appointment_list):#if not reversed, array will skip certian items when removed
            if appointment.appointment_start_date>now:
                appointment_list.remove(appointment)
    else:
        print('No Filter')

    #filters based on what user is searching for
    search=''
    form = SearchForm()
    if form.validate_on_submit():
        search=form.search.data
        if search != '':
            for appointment in reversed(appointment_list):
                if search in appointment.customer_name or search in appointment.appointment_title:
                    print(search, 'found')
                else:
                    appointment_list.remove(appointment)

    count = len(appointment_list)
    return render_template("main/appointmentsearch.html",appointment_list = appointment_list, filterby=filterby,search=search, count=count, form=form)
