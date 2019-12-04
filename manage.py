#from flask.ext.script import Manager, prompt_bool, Shell, Server
from flask_script import Manager, prompt_bool, Shell, Server

from app import db, models, create_app

#from app import create_app

app = create_app()



manager = Manager(app)


def make_shell_context():
    return dict(app=app)


@manager.command
def initdb():
    ''' Create the SQL database. '''
    db.create_all()
    print('The SQL database has been created', 'green')


@manager.command
def dropdb():
    ''' Delete the SQL database. '''
    if prompt_bool('Are you sure you want to lose all your SQL data?'):
        db.drop_all()
        print('The SQL database has been deleted')


manager.add_command('runserver', Server())
manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
